#!/usr/bin/env bash
# Validates every file in examples/ with `esphome config`.
#
# - Complete configurations (containing an `esphome:` block) are validated as-is.
# - Snippets (only the LD2450 block) are wrapped in a minimal ESP32 configuration
#   and use the local component instead of the GitHub source.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work_dir="$(mktemp -d)"
trap 'rm -rf "${work_dir}" "${repo_root}/examples/secrets.yaml"' EXIT

cp "${repo_root}/example-secrets.yaml" "${repo_root}/examples/secrets.yaml"
cp -r "${repo_root}/components" "${work_dir}/components"
cp "${repo_root}/example-secrets.yaml" "${work_dir}/secrets.yaml"

failed=0
for example in "${repo_root}"/examples/*.yaml; do
    name="$(basename "${example}")"
    if [[ "${name}" == "secrets.yaml" ]]; then
        continue
    fi

    if grep -q '^esphome:' "${example}"; then
        target="${example}"
        run_dir="${repo_root}"
    else
        {
            printf 'esphome:\n  name: example\nesp32:\n  board: esp32dev\nlogger:\n  baud_rate: 0\n'
            sed 's#- source: github://.*#- source: {type: local, path: components}#' "${example}"
        } > "${work_dir}/example.yaml"
        target="${work_dir}/example.yaml"
        run_dir="${work_dir}"
    fi

    echo "::group::${name}"
    if (cd "${run_dir}" && esphome config "${target}" > /dev/null); then
        echo "OK: ${name}"
    else
        echo "FAILED: ${name}"
        failed=1
    fi
    echo "::endgroup::"
done

exit "${failed}"
