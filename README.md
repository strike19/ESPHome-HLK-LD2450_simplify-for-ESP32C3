# ESPHome HLK-LD2450 - Vereinfacht für ESP32-C3

Eine vereinfachte ESPHome-Integration für den HLK-LD2450 mmWave Presence Sensor, optimiert für ESP32-C3 Super Mini Boards.

> **Basiert auf:** [TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450)

## 🔧 Behobene Bugs

### 1. `is_convex()` Funktion in `__init__.py`
- **Problem:** Duplizierte Bedingung im Kreuzprodukt-Vergleich für Polygon-Konvexitätsprüfung
- **Status:** Bug existierte, aber die Zonen-Funktionalität wurde komplett entfernt

### 2. `fast_off_detection` Bug in `target.cpp`
- **Problem:** Bei `fast_off_detection` wurde `resolution_ != 0` (alter Wert) geprüft statt auch den neuen Wert zu berücksichtigen. Dadurch wurde `last_change_` nicht aktualisiert wenn ein Target erscheint.
- **Lösung:** Bedingung geändert von:
  ```cpp
  if (fast_off_detection_ && resolution_ != 0 && ...)
  ```
  zu:
  ```cpp
  if (fast_off_detection_ && (resolution != 0 || resolution_ != 0) && ...)
  ```

## ✅ Behaltene Features

### Sensoren (pro Target - max. 3)
- X Position (Meter)
- Y Position (Meter)
- Speed (m/s)
- Distance (Meter)
- Angle (Grad)

### Globale Sensoren
- **Occupancy** (binary_sensor) - Anwesenheitserkennung
- **Target Count** (sensor) - Anzahl erkannter Ziele

### Einstellbare Parameter (Number-Entities)
- **Max Detection Distance** - Maximale Erkennungsdistanz (0-6m)
- **Max Tilt Angle** - Maximaler Neigungswinkel (-90° bis 90°)
- **Min Tilt Angle** - Minimaler Neigungswinkel (-90° bis 90°)

### Steuerung
- **Tracking Mode Switch** - Multi-Target vs. Single-Target Modus
- **Restart Button** - Sensor-Neustart

### Optionale Konfiguration
- `flip_x_axis` - X-Achse spiegeln
- `fast_off_detection` - Schnelle Erkennung wenn Target verschwindet

## ❌ Entfernte Features

- **Zonen** (komplett) - zone.cpp, zone.h gelöscht
- **Factory Reset Button** - Entfernt aus LD2450.cpp/h
- **Bluetooth Switch** - bluetooth_switch.cpp, bluetooth_switch.h gelöscht
- **Baud Rate Select** - baud_rate_select.cpp, baud_rate_select.h gelöscht
- **Distance Resolution Sensor** - Aus target.cpp/h entfernt

## 📁 Gelöschte Dateien

```
components/LD2450/
├── zone.cpp (gelöscht)
├── zone.h (gelöscht)
├── baud_rate_select.cpp (gelöscht)
├── baud_rate_select.h (gelöscht)
├── bluetooth_switch.cpp (gelöscht)
├── bluetooth_switch.h (gelöscht)
└── __pycache__/ (gelöscht)
```

## 📶 WiFi Konfiguration für ESP32-C3

Das ESP32-C3 Super Mini hatte ein bekanntes Problem mit -127 dB WiFi-Signal. Diese optimierte Konfiguration behebt das:

```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  output_power: 8.5dBm     # Kritisch für ESP32-C3 Mini!
  power_save_mode: NONE    # Kein Power-Save für stabile Verbindung
  fast_connect: true       # Schnellere Verbindung
```

## 🔐 Secrets Konfiguration

### 1. Example-Datei kopieren
```bash
cp example-secrets.yaml secrets.yaml
```

### 2. secrets.yaml ausfüllen
```yaml
# WiFi
wifi_ssid: "DEIN_WLAN_NAME"
wifi_password: "DEIN_WLAN_PASSWORT"

# MQTT (für ioBroker)
mqtt_broker: "192.168.1.100"
mqtt_username: "mqtt_user"
mqtt_password: "mqtt_password"

# API & OTA
api_password: "api_passwort"
ota_password: "ota_passwort"
ap_password: "fallback_passwort"
```

> **Hinweis:** `secrets.yaml` ist in `.gitignore` und wird nicht eingecheckt!

## 🚀 Installation

### 1. Repository klonen
```bash
git clone https://github.com/strike19/ESPHome-HLK-LD2450_simplify-for-ESP32C3
cd ESPHome-HLK-LD2450_simplify-for-ESP32C3
```

### 2. Secrets erstellen
```bash
cp example-secrets.yaml secrets.yaml
# secrets.yaml mit deinen Daten ausfüllen
```

### 3. Beispiel-Konfiguration verwenden
```bash
esphome run examples/esp32c3_mqtt_minimal.yaml
```

## 📄 Beispiel-Konfiguration

Siehe `examples/esp32c3_mqtt_minimal.yaml` für eine vollständige, minimale Konfiguration.

### Minimale YAML-Konfiguration

```yaml
external_components:
  - source:
      type: local
      path: components

uart:
  id: uart_ld2450
  tx_pin: GPIO21
  rx_pin: GPIO20
  baud_rate: 256000
  parity: NONE
  stop_bits: 1

LD2450:
  uart_id: uart_ld2450
  name: "Presence"
  fast_off_detection: true
  
  occupancy:
    name: "Occupancy"
  
  target_count:
    name: "Target Count"
  
  targets:
    - target:
        name: "Target 1"
        x_position:
        y_position:
        speed:
        distance:
        angle:

  max_detection_distance:
    name: "Max Distance"
    initial_value: 6m
    
  tracking_mode_switch:
    name: "Multi-Target Mode"
  
  restart_button:
    name: "Restart Sensor"
```

## 🔌 Hardware-Verbindung

### ESP32-C3 Super Mini → HLK-LD2450

| ESP32-C3 | LD2450 |
|----------|--------|
| GPIO21 (TX) | RX |
| GPIO20 (RX) | TX |
| 3.3V | VCC |
| GND | GND |

## 📝 Lizenz

MIT License - siehe [LICENCE](LICENCE)

## 🙏 Credits

- Ursprüngliches Repository: [TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450)
