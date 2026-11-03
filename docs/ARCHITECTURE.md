# System Architecture

## 1. Functional layers

### Sensor and acquisition layer
The STM32L4S5VIT6 on the B-L4S5I-IOT01A development platform is the sensor-side controller. The telemetry fields currently consumed by the host include object/target temperature, ambient temperature, relative humidity, illuminance, CO₂, optional BPM/SpO₂, ultrasonic distance, MQ-2 raw ADC and PIR motion state.

The precise sensor models and pin assignments must be documented from the assembled hardware rather than inferred from the telemetry field names.

### Communication layer
The documented serial/wireless chain is:

1. STM32 UART4 TX on PA0.
2. UART link to ESP32 bridge A GPIO16/RX2, 115200 baud, 8N1, common ground.
3. ESP-NOW transfer from ESP32 A to ESP32 B.
4. USB serial from ESP32 B to the host computer (documented Windows port: COM28, 115200 baud).

### Host application layer
The Python application reads serial data with pyserial, parses JSON, maintains current telemetry and recent history, invokes the risk engine, and serves a local web application.

### Presentation layer
The browser interface has two related views:
- Dashboard: telemetry cards, connection/status information, risk indication and supporting plots/controls.
- Digital twin/visor: Three.js schematic building view, camera controls, first-person-style HUD overlay, alert cue and fixed route illustration.

## 2. Example JSON interface

```json
{
  "device": "SMARTFIRE-X",
  "temp_c": 30.5,
  "ambient_c": 30.4,
  "humidity_pct": 73.8,
  "light_lux": 81.6,
  "co2_ppm": 701,
  "bpm": null,
  "spo2_pct": null,
  "distance_cm": 5.7,
  "mq2_raw": 674,
  "pir": true
}
```

Optional measurements may be null. The parser and UI should preserve missing-data state instead of treating missing values as zero.

## 3. Dashboard data path

1. ESP32 B outputs telemetry over USB serial.
2. Python reads the serial stream.
3. The application decodes each JSON packet and updates the latest state/history.
4. The risk engine evaluates configured rules and data availability.
5. The local HTTP endpoint exposes current state to the browser.
6. JavaScript polls the endpoint approximately every 500 ms and updates the visible interface.

The 500 ms figure is the browser polling interval; it is not a measured end-to-end system latency.

## 4. Risk engine

The risk engine is rule-based, not a trained machine-learning model. It uses configured thresholds, selected combinations and recent trends to produce a score, category and explanations. Evidence coverage is a measure of input availability, not a probability or confidence that the environment is safe.

The visor prototype displays a red alert cue when CO₂ >= 1500 ppm or MQ-2 raw ADC >= 1200. These are demonstration thresholds only and are not certified occupational exposure limits.

## 5. Digital twin

The 3D environment is procedurally assembled in Three.js from geometric objects and materials. It includes a schematic multi-room layout and camera controls. Visor mode hides the avatar image plane, changes the camera presentation and displays selected live readings.

The route is a fixed visual illustration. No real-time position tracking, obstacle detection, pathfinding or evacuation validation is implemented.

## 6. Safety and engineering limitations

- MQ-2 raw ADC does not identify a particular toxic gas.
- Sensor calibration, cross-sensitivity and environmental effects require evaluation.
- The building layout is not a surveyed CAD/BIM model.
- A browser HUD is not a physical optical visor.
- The prototype is not certified PPE or an operational life-safety system.
