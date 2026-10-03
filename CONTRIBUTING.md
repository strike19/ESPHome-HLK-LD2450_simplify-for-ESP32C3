# Regelwerk für dieses Repository

Dieses Dokument legt fest, wie Code, Bezeichner, Kommentare, Dokumentation,
Changelog, Versionen und Commits in diesem Repository gepflegt werden. Es stützt sich auf
etablierte Standards:

- [ESPHome Developer Docs – Contributing](https://developers.esphome.io/contributing/code/) (Code-Stil)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) (Changelog)
- [Semantic Versioning 2.0.0](https://semver.org/) (Versionierung ab `v1.0.0`)
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

## 4. Bezeichner

Ein Name beschreibt, **was** etwas ist, nicht wie es implementiert ist.

- **Aussagekräftig:** Keine Einbuchstaben-Namen außer Schleifenzählern (`i`, `j`)
  und Koordinaten (`x`, `y`). Keine Abkürzungen, die nicht im LD2450-Datenblatt
  oder in ESPHome selbst üblich sind (`uart`, `ms`, `mm` sind ok).
- **Einheiten:** Interne Variablen, deren Einheit nicht aus dem Typ folgt, tragen
  sie im Namen (`distance_mm`, `timeout_ms`, `angle_deg`). Nach außen
  (YAML, Entitäten) gelten die ESPHome-Einheitenkonstanten
  (`UNIT_METER`, `UNIT_DEGREES`); dort KEINE Einheit im Optionsnamen.
- **Booleans:** als Aussage formuliert (`is_`, `has_`, `use_`, `_enabled`),
  nie negiert (`not_connected` → `connected`).
- **Funktionen:** Verb zuerst (`set_`, `get_`, `update_`, `parse_`, `send_`);
  Abfragen ohne Seiteneffekt heißen wie das Ergebnis (`is_convex`).
- **Konstanten:** benannt statt Zahl im Code; Protokollwerte des Sensors mit
  Präfix (`FRAME_HEADER`, `CMD_...`).
- **YAML-Optionen:** `lower_snake_case`, englisch, wie ESPHome-Kernkomponenten
  benannt (`max_detection_distance`, nicht `maxDist`). Die zugehörige
  Python-Konstante heißt `CONF_<OPTION_IN_GROSSBUCHSTABEN>`.
- **Entitäten/Sensoren:** Einheitliches Schema `<Hub-Name> <Objekt> <Größe>`
  (z. B. „Target 1 Distance“); keine Umlaute oder Sonderzeichen in IDs.
- **Dateien:** Komponenten-Dateien `lower_snake_case` (`limit_number.cpp`);
  Header und Quelle teilen sich den Namen; Beispiele in `examples/` beschreiben
  den Zweck (`esp32c3_mqtt_minimal.yaml`).
- **Umbenennen:** Das Umbenennen einer YAML-Option oder Entität ist ein
  Breaking Change (Abschnitt 9) und wird im Changelog vermerkt.

---

## 5. Dead Code

Dead Code ist alles, was kompiliert, aber nie ausgeführt oder benutzt wird.
Er wird **nicht auf Vorrat** behalten; Git bewahrt die Historie.

- **MUSS** entfernt werden: auskommentierter Code, ungenutzte Funktionen,
  Methoden, Member, Parameter, Includes, Konstanten und `#define`s, nicht
  erreichbare Zweige, leere Stubs, verwaiste Dateien (`.cpp`/`.h` ohne
  Verwendung, Beispiele ohne Bezug zu einer existierenden Option).
- **Config-Optionen**, die kein Code mehr auswertet, werden aus
  `__init__.py`, README, Beispielen und Tests gemeinsam entfernt (Breaking
  Change, wenn Nutzer sie setzen konnten).
- Entfernen erfolgt in einem **eigenen Commit** (`refactor: remove unused ...`),
  getrennt von Funktionsänderungen, damit Reverts einfach bleiben.
- Auffinden: Compiler-Warnungen (`-Wunused`) dürfen nicht ignoriert werden;
  vor jedem Release prüfen (`grep` auf Definitionen ohne Verwendung, clang-tidy
  `misc-unused-*`/`readability-redundant-*`, wenn verfügbar).
- Ausnahmen (z. B. Schnittstellen, die ESPHome verlangt, `override`-Methoden mit
  leerem Rumpf) werden mit einem Kurzkommentar begründet.
- **Gelöschten Funktionsumfang** (hier: Zonen) dokumentiert das Changelog unter
  `Removed`, nicht ein Kommentar im Code.

---

## 6. Do's and Don'ts im Code

**Do**

- Eingaben vom Sensor prüfen: Länge, Header und Wertebereich, bevor sie
  verwendet werden. Fehlerhafte Frames verwerfen, nicht interpretieren.
- Fehlerpfade sichtbar machen (`ESP_LOGW`/`ESP_LOGE` mit Ursache) und den
  Zustand sauber zurücksetzen (z. B. RX-Puffer leeren, Config-Mode verlassen).
- Werte aus `__init__.py` über Setter in die C++-Klasse geben; Standardwerte
  stehen im Python-Schema, nicht doppelt im C++.
- Variablen immer initialisieren; `const`/`constexpr` verwenden, wo möglich.
- Neue Optionen in `dump_config()` ausgeben.
- Zeitvergleiche mit `millis()` vorzeichenlos und überlaufsicher
  (`now - last > timeout`).
- Kleine Funktionen mit einer Aufgabe; tief verschachtelte Bedingungen
  durch frühe Rückgaben auflösen.

**Don't**

- Keine Magic Numbers (Frame-Bytes, Timeouts, Schwellwerte): benennen und
  kommentieren.
- Kein `delay()`, keine Endlosschleifen und keine dynamische Allokation
  (`new`, `std::vector`-Wachstum, `String`) in `loop()`/Parsing-Pfaden.
- Kein `ESP_LOGI`/`ESP_LOGD` pro Frame ohne Frequenzbegrenzung.
- Keine globalen veränderlichen Variablen; Zustand gehört in die Klasse.
- Keine stillen `catch`/`if`-Fälle, die Fehler verschlucken.
- Keine Platzhalter-Werte aus Tests oder Beispiel-Zugangsdaten im Produktivcode.
- Keine unbegründeten Änderungen am Upstream-Code (Formatierung,
  Umbenennungen), die künftige Merges erschweren (Abschnitt 10).
- Keine Compiler-Warnungen unterdrücken, um CI grün zu bekommen.

---

## 7. Dokumentation

- `README.md` ist die einzige Nutzerdokumentation und MUSS aktuell sein bei
  jeder Änderung an Optionen, Verhalten, Beispielen oder Hardware-Hinweisen.
- Jede **Konfigurationsoption** MUSS im README mit Typ, Pflicht/Optional,
  Standardwert und kurzer Beschreibung stehen.
- Jede **neue Funktion** bekommt ein Beispiel in `examples/`.
- Dokumentation wird **sachlich** und ohne Emojis als Gliederung geschrieben;
  Warnhinweise (z. B. „ungetestet“) stehen als Blockquote am Anfang.
- Das README nennt den **Upstream** (Quelle, Lizenz) und die Abweichungen davon.
- Änderungsverlauf gehört ins Changelog (Abschnitt 8), nicht ins README.
- Dateinamen: Markdown in `UPPER_CASE.md` für Projektdateien
  (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`), sonst `lower-case`.

---

## 8. Changelog

Format: **Keep a Changelog 1.1.0**, Datei `CHANGELOG.md` im Repo-Root.

- Es gibt **genau eine** Changelog-Datei. Neue Einträge MÜSSEN dort landen.
- Oben steht immer der Abschnitt `## [Unreleased]`.
- Pro Release ein Abschnitt `## [<Build oder X.Y.Z>] - JJJJ-MM-TT` (ISO 8601), neueste zuerst (Schema siehe Abschnitt 9).
- Gruppierung ausschließlich nach: `Added`, `Changed`, `Deprecated`, `Removed`,
  `Fixed`, `Security`.
- Einträge sind für **Nutzer** geschrieben (Auswirkung, nicht Implementierung),
  ein Eintrag pro Zeile, mit Verweis auf Issue/PR, falls vorhanden.
- Breaking Changes werden unter `Changed`/`Removed` mit dem Präfix **BREAKING:**
  markiert und erklären den Migrationsweg.
- Am Dateiende stehen Vergleichslinks (`[Unreleased]: .../compare/<letzter-Tag-oder-Hash>...HEAD`).
- Einträge des Upstream werden nicht kopiert; der Changelog beschreibt nur die
  Änderungen dieses Forks. Die Upstream-Basis wird je Release genannt
  (z. B. „Basiert auf Upstream v1.0.6“).

---

## 9. Versionierung

Dieses Projekt verwendet eine **fortlaufende Build-Nummer** statt manuell
gepflegter Versionsnummern.

- **Build-Nummer:** Anzahl der Commits auf `main`
  (`git rev-list --count main`). Sie ist automatisch, eindeutig und muss nicht
  gepflegt werden. Anzeige zusammen mit dem Kurz-Hash, z. B. `b142-9e1c6b4`
  oder über `git describe --tags --always`.
- Commits auf `main` entstehen ausschließlich per Merge/Squash eines Pull
  Requests, damit die Historie linear und die Nummer stabil bleibt. Die Historie
  von `main` wird **nie** umgeschrieben.
- Die Zählung beginnt nicht neu; die geerbten Upstream-Commits zählen mit.
- **Meilenstein `v1.0.0`:** Sobald das Projekt auf realer Hardware (ESP32-C3 +
  HLK-LD2450) getestet und der Warnhinweis im README entfernt ist, wird
  `v1.0.0` als annotierter Tag gesetzt und ein GitHub Release erstellt.
- **Nach `v1.0.0`:** Weitere Releases werden als Tag `vX.Y.Z` (SemVer) auf einen
  Build gesetzt. MAJOR = inkompatible Änderung an YAML-Optionen, Entity-Namen
  oder MQTT-Topics; MINOR = neue abwärtskompatible Funktion; PATCH = Fehlerbehebung.
  Die Build-Nummer läuft unabhängig weiter.
- Getaggte Versionen werden nie verschoben oder gelöscht.
- **Changelog:** Einträge unter `[Unreleased]`; beim Release in den Abschnitt
  des Tags umbenennen. Vor `v1.0.0` darf der Abschnitt statt der Version
  die Build-Nummer und das Datum tragen (`## [b142] - JJJJ-MM-TT`); das
  gewählte Schema steht im Kopf von `CHANGELOG.md`.

---

## 10. Commits, Branches, Pull Requests

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

## 11. Definition of Done

Eine Änderung ist fertig, wenn:

1. Der Code kompiliert (CI grün) und `pre-commit` keine Befunde hat.
2. Neue/geänderte Optionen im README und in einem Beispiel stehen.
3. Der Changelog unter `[Unreleased]` ergänzt ist.
4. Kommentare, Bezeichner und Do's/Don'ts den Abschnitten 3–6 entsprechen
   und kein Dead Code (Abschnitt 5) verbleibt.
5. Die Commit-Nachrichten Abschnitt 10 entsprechen.
