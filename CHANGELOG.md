# Changelog

Alle nennenswerten Änderungen dieses Forks werden hier dokumentiert.

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Versionsschema: fortlaufende Build-Nummer (Commit-Anzahl auf `main`) bis
`v1.0.0`, danach [Semantic Versioning](https://semver.org/) – siehe
[CONTRIBUTING.md](CONTRIBUTING.md), Abschnitt 9.

Die Änderungen des Upstream-Projekts
([TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450),
zuletzt `v1.0.6`) sind hier nicht aufgeführt.

## [Unreleased]

Basiert auf Upstream `v1.0.6`. Das Projekt ist noch nicht auf Hardware getestet.

### Added

- Beispielkonfiguration `examples/esp32c3_mqtt_minimal.yaml` für ESP32-C3 Super
  Mini mit MQTT (ioBroker) und angepassten WiFi-Einstellungen
  (`output_power`, `power_save_mode`, `fast_connect`).
- `example-secrets.yaml` als Vorlage für WiFi-, MQTT-, API- und OTA-Zugangsdaten.
- `CONTRIBUTING.md` mit Regeln für Code, Dokumentation, Changelog, Versionierung
  und Commits.
- `CHANGELOG.md` (dieses Dokument); es ersetzt `CHANGES.md` und
  `CHANGES_SUMMARY.md`.

### Changed

- **BREAKING:** Die Komponente ist auf drei Targets, Occupancy, Target Count,
  die Grenzwert-Entitäten, den Tracking-Mode-Schalter und den Restart-Button
  reduziert.
- `README.md` neu strukturiert (Installation, Optionsreferenz, Hardware).
- Beispiele laden die Komponente aus diesem Fork statt aus dem Upstream.
- Konstanten in `LD2450.h` und `target.h` sind typisierte `constexpr`-Werte
  statt `#define`.
- `secrets.yaml` wird in jedem Verzeichnis von Git ignoriert (nicht nur im
  Root), damit sie neben den Beispielen liegen kann.

### Removed

- **BREAKING:** Zonen (Polygon-Zonen, Template-Polygone, `zones`-Option).
- **BREAKING:** `factory_reset_button`, `bluetooth_switch`, `baud_rate_select`
  und der Target-Sensor `distance_resolution`.
- Beispiele `examples/zones.yaml` und `examples/editable_template_polygon.yaml`,
  das Bild `zone_sketch.png` und die Zonen-Abschnitte in `tests/full.yaml` und
  `examples/full.yaml` (Zonen existieren nicht mehr).
- Doppelte Konfiguration `ld2450-minimal.yaml` (identisch zu
  `examples/esp32c3_mqtt_minimal.yaml`).

### Fixed

- `fast_off_detection`: Ein neu erscheinendes Target setzt `last_change_` nun
  korrekt (geprüft werden alter und neuer `resolution`-Wert).
- `tests/full.yaml` und die Beispiele validieren wieder mit aktuellem ESPHome;
  der `ota`-Eintrag in `examples/esp32c3_mqtt_minimal.yaml` enthält jetzt
  `platform: esphome`.
- Die Minimalkonfiguration im README validiert wieder (leere Sensor-Einträge
  sind mit aktuellem ESPHome ungültig und tragen jetzt einen `name`).

[Unreleased]: https://github.com/strike19/ESPHome-HLK-LD2450_simplify-for-ESP32C3/commits/main
