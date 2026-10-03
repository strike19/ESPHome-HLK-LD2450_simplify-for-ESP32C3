# Regelwerk für dieses Repository

Dieses Dokument legt fest, wie Code, Kommentare, Dokumentation, Changelog,
Versionen und Commits in diesem Repository gepflegt werden. Es stützt sich auf
etablierte Standards:

- [ESPHome Developer Docs – Contributing](https://developers.esphome.io/contributing/code/) (Code-Stil)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) (Changelog)
- [Semantic Versioning 2.0.0](https://semver.org/) (Versionierung)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) (Commit-Nachrichten)

Sprache: **Dokumentation auf Deutsch, Code, Code-Kommentare, Commit-Nachrichten
und Bezeichner auf Englisch.** Grund: Die Doku richtet sich an die Nutzer des
Forks, der Code bleibt mit dem Upstream (TillFleisch/ESPHome-HLK-LD2450)
vergleichbar und mergebar.

Die Regeln sind mit **MUSS** (verbindlich, wird in CI/pre-commit geprüft, soweit
möglich), **SOLL** (Standard, Abweichung begründen) und **KANN** (optional)
gekennzeichnet.

---

## 1. Automatische Prüfungen

Formatierung wird von Werkzeugen erzwungen, nicht von Reviews. Konfiguration
liegt im Repo und ist die Referenz:

| Bereich      | Werkzeug     | Konfiguration          |
| ------------ | ------------ | ---------------------- |
| C++          | clang-format | `.clang-format`        |
| Python       | black, isort | `pyproject.toml`       |
| YAML         | yamllint     | `.yamllint`            |
| Kompilierung | ESPHome      | `tests/base.yaml`, `tests/full.yaml` |

- Vor jedem Commit MUSS `pre-commit run --all-files` fehlerfrei laufen.
- Ein Pull Request darf nur gemergt werden, wenn die CI (`.github/workflows/ci.yaml`) grün ist.
- Neue Funktionen MÜSSEN in `tests/full.yaml` (und, falls Pflichtoption, in
  `tests/base.yaml`) kompilieren; die CI ist der einzige automatische Test.

---

## 2. Code-Regeln

Grundlage ist der ESPHome-Stil (Google C++ Style Guide mit Anpassungen). Wo
`.clang-format` davon abweicht (Allman-Klammern, 4 Leerzeichen), gilt
`.clang-format`.

### C++

- **Namen:** Funktionen, Methoden, Variablen `lower_snake_case`; Klassen, Structs,
  Enums `UpperCamelCase`; Konstanten `UPPER_SNAKE_CASE`.
- **Member:** `lower_snake_case_` mit Unterstrich am Ende. SOLL `protected` statt
  `private` sein, außer bei echten Implementierungsdetails.
- **Zugriff:** Auf Member SOLL mit `this->` zugegriffen werden (ESPHome-Konvention).
- **Konstanten:** SOLLEN als `static constexpr`/`const` definiert werden, nicht
  per `#define`. `#define` nur für bedingte Kompilierung oder Werte, die der
  Python-Codegen erzeugt.
- **Header:** `#pragma once`; Includes nur, was benötigt wird.
- **Namespace:** `esphome::ld2450`.
- **Logging:** Nur `ESP_LOGx` mit einem `static const char *const TAG`. Kein
  Logging mit hoher Frequenz auf Level `INFO` oder höher; Debug-Ausgaben nur
  über die Debug-Option der Komponente.
- **Ressourcen:** Keine dynamische Speicherallokation in `loop()`; kein
  blockierendes Warten (`delay`) im Hauptthread; UART-Lesen darf `loop()` nie
  festsetzen (Timeouts verwenden).
- **Zeilenlänge:** SOLL ≤ 120 Zeichen (derzeit nicht von clang-format erzwungen).

### Python (`__init__.py`)

- Schema-Schlüssel nutzen vorhandene `CONF_*`-Konstanten aus `esphome.const`,
  bevor eigene definiert werden.
- Konfigurationsfehler werden mit `cv.Invalid` und einer verständlichen,
  englischen Meldung gemeldet.
- black/isort-Formatierung ohne Ausnahmen.

### YAML (Beispiele, Tests)

- Jede Datei in `examples/` MUSS mit `example-secrets.yaml` kompilieren.
- Keine echten Zugangsdaten, IPs oder Passwörter im Repo; nur Platzhalter.

---

## 3. Kommentare im Code

- Sprache Englisch.
- **Öffentliche API** (Klassen, Setter, Methoden in Headern) wird mit
  Doxygen-Blöcken dokumentiert (`/** @brief ... */`), wie bereits in `target.h`.
- **Inline-Kommentare** erklären das *Warum*, nicht das *Was*. Offensichtliches
  wird nicht kommentiert.
- Protokoll-Details des LD2450 (Frame-Header, Byte-Layout, Einheiten) SOLLEN
  direkt am Parsing-Code dokumentiert sein, da sie nicht aus dem Code ableitbar sind.
- Workarounds und Bugfixes tragen einen Kurzkommentar mit Grund und, falls
  vorhanden, Verweis auf Issue/PR.
- `TODO(name):` nur mit Namen und Anlass; kein auskommentierter Code im Repo
  (Git bewahrt die Historie).
- Keine Änderungshistorie im Code (`// fixed 2026-01-18 ...`); dafür gibt es
  Changelog und Commits.

---

## 4. Dokumentation

- `README.md` ist die einzige Nutzerdokumentation und MUSS aktuell sein bei
  jeder Änderung an Optionen, Verhalten, Beispielen oder Hardware-Hinweisen.
- Jede **Konfigurationsoption** MUSS im README mit Typ, Pflicht/Optional,
  Standardwert und kurzer Beschreibung stehen.
- Jede **neue Funktion** bekommt ein Beispiel in `examples/`.
- Dokumentation wird **sachlich** und ohne Emojis als Gliederung geschrieben;
  Warnhinweise (z. B. „ungetestet“) stehen als Blockquote am Anfang.
- Das README nennt den **Upstream** (Quelle, Lizenz) und die Abweichungen davon.
- Änderungsverlauf gehört ins Changelog (Abschnitt 5), nicht ins README.
- Dateinamen: Markdown in `UPPER_CASE.md` für Projektdateien
  (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`), sonst `lower-case`.

---

## 5. Changelog

Format: **Keep a Changelog 1.1.0**, Datei `CHANGELOG.md` im Repo-Root.

- Es gibt **genau eine** Changelog-Datei. Neue Einträge MÜSSEN dort landen.
- Oben steht immer der Abschnitt `## [Unreleased]`.
- Pro Release ein Abschnitt `## [X.Y.Z] - JJJJ-MM-TT` (ISO 8601), neueste zuerst.
- Gruppierung ausschließlich nach: `Added`, `Changed`, `Deprecated`, `Removed`,
  `Fixed`, `Security`.
- Einträge sind für **Nutzer** geschrieben (Auswirkung, nicht Implementierung),
  ein Eintrag pro Zeile, mit Verweis auf Issue/PR, falls vorhanden.
- Breaking Changes werden unter `Changed`/`Removed` mit dem Präfix **BREAKING:**
  markiert und erklären den Migrationsweg.
- Am Dateiende stehen Vergleichslinks (`[Unreleased]: .../compare/vX.Y.Z...HEAD`).
- Einträge des Upstream werden nicht kopiert; der Changelog beschreibt nur die
  Änderungen dieses Forks. Die Upstream-Basis wird je Release genannt
  (z. B. „Basiert auf Upstream v1.0.6“).

---

## 6. Versionierung

Format: **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`), Tags mit Präfix `v`.

- Solange der Fork ungetestet ist, gilt `0.y.z` (alles darf sich ändern);
  `1.0.0` erst nach Hardware-Test auf dem ESP32-C3.
- **MAJOR:** inkompatible Änderung an YAML-Optionen, Entity-Namen oder
  MQTT-Topics (auch Entfernen von Funktionen).
- **MINOR:** neue, abwärtskompatible Funktion oder Option.
- **PATCH:** reine Fehlerbehebung, Doku- oder Beispielkorrektur mit
  Verhaltensrelevanz.
- Release-Ablauf: `[Unreleased]` im Changelog in neue Version umbenennen →
  Commit `chore(release): vX.Y.Z` → annotierter Tag `vX.Y.Z` → GitHub Release
  mit Changelog-Auszug.
- Getaggte Versionen werden nie verschoben oder gelöscht; Fehler werden durch
  ein neues Patch-Release behoben.

---

## 7. Commits, Branches, Pull Requests

**Commit-Nachrichten** nach Conventional Commits (englisch, Imperativ):

```
<type>(<scope>): <kurze Beschreibung, max. 72 Zeichen>

<optionaler Body: Warum, nicht Was>

<optionaler Footer: Closes #12 / BREAKING CHANGE: ...>
```

- Typen: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
  `ci`, `chore`.
- Scopes (Beispiele): `target`, `uart`, `config`, `readme`, `examples`, `ci`.
- Mapping auf SemVer: `fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` bzw.
  `!` hinter dem Typ → MAJOR.
- Ein Commit = eine logische Änderung; Formatierungsänderungen nicht mit
  Funktionsänderungen mischen.

**Branches:** `main` ist stets baubar. Arbeit auf Kurzzeit-Branches
(`feat/...`, `fix/...`, `docs/...`), Merge per Pull Request.

**Pull Requests:**

- Beschreibung: Was, Warum, wie getestet (Hardware ja/nein).
- Checkliste vor dem Merge: CI grün · pre-commit sauber · README aktualisiert ·
  Changelog-Eintrag unter `[Unreleased]` · Beispiel ergänzt (bei neuer Funktion).

**Upstream-Pflege:** Regelmäßig prüfen, ob Upstream neue Commits hat
(`git fetch` auf TillFleisch/ESPHome-HLK-LD2450). Übernahme per Merge oder
Cherry-Pick mit Hinweis im Changelog. Fehlerbehebungen, die auch Upstream
betreffen, werden dort als Pull Request angeboten.

---

## 8. Definition of Done

Eine Änderung ist fertig, wenn:

1. Der Code kompiliert (CI grün) und `pre-commit` keine Befunde hat.
2. Neue/geänderte Optionen im README und in einem Beispiel stehen.
3. Der Changelog unter `[Unreleased]` ergänzt ist.
4. Kommentare dem Abschnitt 3 entsprechen.
5. Die Commit-Nachrichten Abschnitt 7 entsprechen.
