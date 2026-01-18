# CHANGES.md - ESPHome HLK-LD2450 Vereinfacht für ESP32-C3

**Datum:** 18. Januar 2026  
**Basis-Repository:** [TillFleisch/ESPHome-HLK-LD2450](https://github.com/TillFleisch/ESPHome-HLK-LD2450)  
**Ziel:** Minimale Integration für HLK-LD2450 mmWave Presence Sensor mit ESP32-C3 Super Mini und ioBroker MQTT

---

## 📋 Zusammenfassung der Änderungen

### Phase 1: Code-Analyse & Validierung

#### Bug #1: `is_convex()` Funktion in `__init__.py`
- **Ursprünglicher Bug (Zeile 240-243):** 
  ```python
  if cross_product > 0:
      return False
  ```
- **Korrekter Code sollte sein:**
  ```python
  if cross_product < 0:
      return False
  ```
- **Status:** Bug existierte im Original-Repository in der Zonen-Funktionalität
- **Lösung:** Die komplette Zonen-Funktionalität wurde entfernt, wodurch der Bug eliminiert wurde

#### Bug #2: `fast_off_detection` in `target.cpp`
- **Problem:** Bei aktiviertem `fast_off_detection` wurde nur `resolution_ != 0` (alter Wert) geprüft. Der neue `resolution` Wert wurde ignoriert, was dazu führte, dass `last_change_` nicht aktualisiert wurde wenn ein Target erstmals erscheint.
- **Ursprünglicher Code:**
  ```cpp
  if (fast_off_detection_ && resolution_ != 0 && 
      (x != x_ || y != y_ || speed != speed_ || resolution != resolution_))
      last_change_ = millis();
  ```
- **Korrigierter Code:**
  ```cpp
  // Fixed: Check both old AND new resolution to handle target appearance
  if (fast_off_detection_ && (resolution != 0 || resolution_ != 0) &&
      (x != x_ || y != y_ || speed != speed_ || resolution != resolution_))
      last_change_ = millis();
  ```
- **Status:** ✅ Bereits gefixt (mit Kommentar dokumentiert)

#### Abhängigkeiten im `components/LD2450/` Verzeichnis

| Datei | Abhängigkeit | Funktion |
|-------|--------------|----------|
| `__init__.py` | ESPHome Python | Konfiguration, Schema-Validierung, Code-Generation |
| `LD2450.cpp/h` | UART, target.h | Hauptkomponente, UART-Kommunikation |
| `target.cpp/h` | polling_sensor.h | Target-Tracking, Sensor-Werte |
| `polling_sensor.h` | sensor.h | Polling-Sensor für Positionsdaten |
| `limit_number.cpp/h` | LD2450.h | Number-Entities für Limits |
| `tracking_mode_switch.cpp/h` | LD2450.h | Multi/Single-Target Switch |

---

### Phase 2: Code-Bereinigung

#### Entfernte Funktionen aus `__init__.py`
- ❌ Zonen-Code (komplett entfernt)
- ❌ Factory Reset Button Code
- ❌ Bluetooth Switch Code
- ❌ Baud Rate Select Code
- ❌ `distance_resolution` Sensor Code

#### Gelöschte Dateien
```
components/LD2450/
├── zone.cpp           (gelöscht)
├── zone.h             (gelöscht)
├── baud_rate_select.cpp    (gelöscht)
├── baud_rate_select.h      (gelöscht)
├── bluetooth_switch.cpp    (gelöscht)
├── bluetooth_switch.h      (gelöscht)
└── __pycache__/            (gelöscht)
```

#### Behaltene Features ✅

**Target-Sensoren (pro Target, max. 3):**
- X Position (Meter)
- Y Position (Meter)
- Speed (m/s)
- Distance (Meter)
- Angle (Grad)

**Globale Sensoren:**
- `occupancy` (binary_sensor) - Anwesenheitserkennung
- `target_count` (sensor) - Anzahl erkannter Ziele

**Number-Entities:**
- `max_detection_distance` - Maximale Erkennungsdistanz (0-6m)
- `max_detection_tilt_angle` - Maximaler Neigungswinkel (-90° bis 90°)
- `min_detection_tilt_angle` - Minimaler Neigungswinkel (-90° bis 90°)

**Steuerung:**
- `tracking_mode_switch` - Multi-Target vs. Single-Target Modus
- `restart_button` - Sensor-Neustart

**Optionen:**
- `flip_x_axis` - X-Achse spiegeln
- `fast_off_detection` - Schnelle Erkennung bei Target-Verlust

---

### Phase 3: WiFi & Secrets Konfiguration

#### Neue Datei: `secrets.yaml`
```yaml
# WiFi Konfiguration
wifi_ssid: "DEIN_WIFI_SSID"
wifi_password: "DEIN_WIFI_PASSWORT"

# MQTT Konfiguration (für ioBroker Integration)
mqtt_broker: "DEIN_MQTT_BROKER"
mqtt_username: "DEIN_MQTT_USER"
mqtt_password: "DEIN_MQTT_PASSWORT"

# Sicherheit
api_password: "your_api_password"
ota_password: "your_ota_password"
ap_password: "fallback_ap_password"
```

#### ESP32-C3 WiFi-Optimierung
Das ESP32-C3 Super Mini hat ein bekanntes Problem mit -127 dB WiFi-Signal. Die optimierte Konfiguration:

```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  output_power: 8.5dBm     # Kritisch für ESP32-C3 Mini!
  power_save_mode: NONE    # Kein Power-Save für stabile Verbindung
  fast_connect: true       # Schnellere Verbindung
  ap:
    ssid: "c3-wifi-test-fallback"
    password: ""           # Offenes Fallback-Netzwerk
```

#### Aktualisierte Datei: `examples/esp32c3_mqtt_minimal.yaml`
- WiFi-Konfiguration auf ESP32-C3 optimiert
- Fallback AP auf offenes Netzwerk geändert (`c3-wifi-test-fallback`)

---

### Phase 4: Stub-Elimination & Finalisierung

#### Analyse der verbleibenden Komponenten-Dateien

| Datei | Status | Begründung |
|-------|--------|------------|
| `polling_sensor.h` | ✅ Behalten | Benötigt für Target-Sensoren (X, Y, Speed, etc.) |
| `limit_number.cpp/h` | ✅ Behalten | Benötigt für Number-Entities (Max Distance, Angles) |
| `tracking_mode_switch.cpp/h` | ✅ Behalten | Benötigt für Tracking Mode Switch |
| `target.cpp/h` | ✅ Behalten | Core Target-Funktionalität |
| `LD2450.cpp/h` | ✅ Behalten | Hauptkomponente |
| `__init__.py` | ✅ Behalten | ESPHome Konfiguration |

**Ergebnis:** Keine Stub-Files vorhanden. Alle Dateien sind funktional erforderlich.

#### Neue Datei: `ld2450-minimal.yaml`
Minimale Konfigurationsdatei im Root-Verzeichnis mit:
- ESP32-C3 Board-Konfiguration
- Optimierte WiFi-Einstellungen
- MQTT für ioBroker
- 3 Targets mit allen Sensoren
- Alle Number-Entities
- Tracking Mode Switch und Restart Button

---

### Phase 5: Dokumentation

#### Aktualisierte `README.md`
- ✅ Abschnitt "Behobene Bugs" mit Details zu beiden Bugs
- ✅ Abschnitt "Entfernte Features" mit Begründung
- ✅ Abschnitt "WiFi-Konfiguration für ESP32-C3"
- ✅ Anleitung für secrets.yaml Setup
- ✅ Aktualisierte Liste der verfügbaren Features
- ✅ Hinweis auf minimales Ziel: max. 3 Targets

---

## 📁 Finale Projektstruktur

```
ESPHome-HLK-LD2450_simplify-for-ESP32C3/
├── components/
│   └── LD2450/
│       ├── __init__.py         # ESPHome Konfiguration (bereinigt)
│       ├── LD2450.cpp          # Hauptkomponente
│       ├── LD2450.h
│       ├── target.cpp          # Target-Tracking (Bug gefixt)
│       ├── target.h
│       ├── polling_sensor.h    # Sensor-Polling
│       ├── limit_number.cpp    # Number-Entities
│       ├── limit_number.h
│       ├── tracking_mode_switch.cpp
│       └── tracking_mode_switch.h
├── examples/
│   ├── basic.yaml
│   ├── esp32c3_mqtt_minimal.yaml   # (WiFi aktualisiert)
│   ├── full.yaml
│   ├── target_sensors.yaml
│   └── zones.yaml                   # (Legacy, nicht verwendet)
├── tests/
│   ├── base.yaml
│   └── full.yaml
├── ld2450-minimal.yaml         # NEU: Minimale Konfiguration
├── secrets.yaml                # NEU: Credentials (nicht in Git)
├── example-secrets.yaml        # Vorlage für secrets.yaml
├── README.md                   # Aktualisiert
├── CHANGES.md                  # NEU: Diese Datei
├── LICENCE
└── .gitignore                  # Enthält secrets.yaml
```

---

## 🔌 Hardware-Setup

### ESP32-C3 Super Mini → HLK-LD2450

| ESP32-C3 Pin | LD2450 Pin |
|--------------|------------|
| GPIO21 (TX)  | RX         |
| GPIO20 (RX)  | TX         |
| 3.3V         | VCC        |
| GND          | GND        |

---

## ⚡ Quick Start

```bash
# 1. Repository klonen
git clone https://github.com/strike19/ESPHome-HLK-LD2450_simplify-for-ESP32C3
cd ESPHome-HLK-LD2450_simplify-for-ESP32C3

# 2. Secrets erstellen
cp example-secrets.yaml secrets.yaml
# secrets.yaml mit eigenen Daten ausfüllen

# 3. Flashen
esphome run ld2450-minimal.yaml
```

---

## 📝 Changelog

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0.0 | 2026-01-18 | Initial Release: Bereinigte Version für ESP32-C3 |
