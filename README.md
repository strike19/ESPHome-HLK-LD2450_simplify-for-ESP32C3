# ESPHome HLK-LD2450 – vereinfacht für ESP32-C3

Vereinfachte ESPHome-Komponente für den HLK-LD2450 mmWave-Präsenzsensor,
ausgelegt auf ESP32-C3-Super-Mini-Boards und MQTT (z. B. ioBroker).

> **Achtung:** Dieses Projekt ist noch nicht auf Hardware getestet und in
> Entwicklung. Optionen und Entitäten können sich ändern.

Basiert auf [TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450)
(Upstream-Stand `v1.0.6`, MIT-Lizenz). Gegenüber dem Upstream sind unter anderem
Zonen, Factory-Reset, Bluetooth-Schalter und Baudraten-Auswahl entfernt; die
vollständige Liste steht im [Changelog](CHANGELOG.md).

## Funktionsumfang

| Bereich | Entitäten / Optionen |
| --- | --- |
| Pro Target (max. 3) | X-Position, Y-Position, Geschwindigkeit, Distanz, Winkel |
| Global | Occupancy (`binary_sensor`), Target Count (`sensor`) |
| Einstellbare Grenzwerte (`number`) | maximale Distanz, minimaler und maximaler Neigungswinkel |
| Steuerung | Tracking-Mode-Schalter (Multi-/Single-Target), Restart-Button |
| Verhalten | `flip_x_axis`, `fast_off_detection` |

## Hardware

| ESP32-C3 | LD2450 |
| --- | --- |
| GPIO21 (TX) | RX |
| GPIO20 (RX) | TX |
| 3,3 V | VCC |
| GND | GND |

Der UART-Logger muss deaktiviert sein (`logger: baud_rate: 0`), da der UART
für den Sensor benötigt wird.

## Installation

1. Repository klonen:

   ```bash
   git clone https://github.com/strike19/ESPHome-HLK-LD2450_simplify-for-ESP32C3
   cd ESPHome-HLK-LD2450_simplify-for-ESP32C3
   ```

2. Zugangsdaten anlegen. `secrets.yaml` muss neben der YAML-Datei liegen, die
   sie verwendet, und wird von Git ignoriert:

   ```bash
   cp example-secrets.yaml examples/secrets.yaml
   # examples/secrets.yaml mit den eigenen Werten ausfüllen
   ```

3. Beispiel flashen:

   ```bash
   esphome run examples/esp32c3_mqtt_minimal.yaml
   ```

Die Beispielkonfiguration `examples/esp32c3_mqtt_minimal.yaml` enthält WiFi
(inkl. ESP32-C3-Einstellungen), MQTT, OTA, UART und alle Entitäten. Weitere
Beispiele in `examples/` zeigen nur den `LD2450:`-Block und müssen in eine
vollständige Konfiguration eingebettet werden.

### WiFi beim ESP32-C3 Super Mini

Einige Boards zeigen ein sehr schwaches WiFi-Signal (-127 dB). Abhilfe schafft
eine reduzierte Sendeleistung:

```yaml
wifi:
  output_power: 8.5dBm
  power_save_mode: NONE
  fast_connect: true
```

### Minimale Konfiguration

```yaml
external_components:
  - source: github://strike19/ESPHome-HLK-LD2450_simplify-for-ESP32C3@main

uart:
  id: uart_ld2450
  tx_pin: GPIO21
  rx_pin: GPIO20
  baud_rate: 256000
  parity: NONE
  stop_bits: 1

LD2450:
  uart_id: uart_ld2450
  fast_off_detection: true
  occupancy:
    name: "Occupancy"
  target_count:
    name: "Target Count"
  targets:
    - target:
        name: "Target 1"
        x_position:
          name: "X"
        y_position:
          name: "Y"
        speed:
          name: "Speed"
        distance:
          name: "Distance"
        angle:
          name: "Angle"
  max_detection_distance:
    name: "Max Distance"
    initial_value: 6m
  tracking_mode_switch:
    name: "Multi-Target Mode"
  restart_button:
    name: "Restart Sensor"
```

## Optionsreferenz

### `LD2450:`

| Option | Typ | Standard | Beschreibung |
| --- | --- | --- | --- |
| `uart_id` | ID | – (Pflicht) | UART-Bus, an dem der Sensor hängt |
| `name` | String | `LD2450` | Name der Komponente (Logausgabe) |
| `targets` | Liste, 1–3 Einträge | – | Targets, siehe unten |
| `flip_x_axis` | bool | `false` | Spiegelt die X-Achse |
| `fast_off_detection` | bool | `false` | Meldet „nicht belegt“ schneller, wenn sich ein Target nicht mehr ändert |
| `occupancy` | `binary_sensor` | – | Anwesenheit |
| `target_count` | `sensor` | – | Anzahl erkannter Targets |
| `max_detection_distance` | Distanz oder `number` | – | Maximale Erkennungsdistanz, 0–6 m; als `number` mit `initial_value` (Standard `6m`), `step` (`10cm`), `restore_value` (`true`) |
| `max_detection_tilt_angle` | Winkel oder `number` | – | Maximaler Neigungswinkel, -90° bis 90°; als `number`: `initial_value` `90°`, `step` `1°`, `restore_value` `true` |
| `min_detection_tilt_angle` | Winkel oder `number` | – | Minimaler Neigungswinkel, -90° bis 90°; als `number`: `initial_value` `-90°`; muss kleiner sein als der maximale Winkel |
| `max_distance_margin` | Distanz, 0–6 m | `25cm` | Toleranz an der Distanzgrenze |
| `tilt_angle_margin` | Winkel, 0°–45° | `5°` | Toleranz an den Winkelgrenzen |
| `tracking_mode_switch` | `switch` | – | Multi- oder Single-Target-Tracking |
| `restart_button` | `button` | – | Startet den Sensor neu |

### `targets:` → `- target:`

| Option | Typ | Standard | Beschreibung |
| --- | --- | --- | --- |
| `name` | String | `Target <n>` | Namenspräfix der Sensoren |
| `debug` | bool | `false` | Gibt Rohwerte im Log aus |
| `x_position`, `y_position`, `distance` | `sensor` | – | Meter (`unit_of_measurement`: `m` oder `cm`) |
| `speed` | `sensor` | – | Meter pro Sekunde |
| `angle` | `sensor` | – | Grad |

Die Sensoren sind Polling-Sensoren mit `update_interval: 1s` als Standard.

## Entwicklung

Regeln für Code, Dokumentation, Changelog, Versionierung und Commits stehen in
[CONTRIBUTING.md](CONTRIBUTING.md). Änderungen werden im
[Changelog](CHANGELOG.md) festgehalten.

## Lizenz und Quellen

MIT-Lizenz, siehe [LICENCE](LICENCE). Ursprüngliches Projekt:
[TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450).
