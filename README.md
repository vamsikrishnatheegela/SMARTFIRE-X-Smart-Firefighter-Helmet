# SMARTFIRE-X — Smart Firefighter Helmet

An embedded-IoT prototype that brings together environmental sensing, wireless telemetry, a live monitoring dashboard, rule-based risk indication, and a browser-based 3D building digital twin with a visor-style HUD.

> **Prototype and safety notice:** SMARTFIRE-X is an academic engineering prototype. It is not certified personal protective equipment, a gas detector, a fire alarm, or a validated evacuation/navigation system. Do not use it as the sole basis for firefighting, exposure decisions, or emergency evacuation.

## Project overview

SMARTFIRE-X is organized into three main layers:

1. **Embedded sensing and acquisition** — an STM32L4S5VIT6 on the B-L4S5I-IOT01A platform acquires sensor information and formats telemetry.
2. **Communication bridge** — UART connects the STM32 to ESP32 bridge A; ESP-NOW forwards the data to ESP32 bridge B, which presents it to the host computer over USB serial.
3. **Host software and visualization** — a Python application reads serial telemetry, evaluates prototype risk rules, serves a local web interface, and presents a dashboard plus a Three.js-based 3D building/visor view.

## System architecture

```text
Environmental / proximity / optional physiological sensors
                         |
                         v
             STM32L4S5VIT6 development board
                 UART4 TX (PA0)
                         |
                 UART 115200, 8N1
                         |
                         v
              ESP32 bridge A (GPIO16/RX2)
                         |
                     ESP-NOW
                         |
                         v
              ESP32 bridge B (receiver)
                         |
                  USB serial / COM28
                         |
                         v
             Python host application
        pyserial -> JSON parser -> state/history
                         |
              +----------+----------+
              |                     |
              v                     v
       Rule-based risk engine   Local HTTP server
                                    |
                                    v
                         Browser dashboard / HUD
                                    |
                         Three.js building twin
```

## Sensor channels

The telemetry schema used by the host application includes:

| Field | Meaning | Notes |
|---|---|---|
| `temp_c` | Object/target temperature in °C | Confirm exact sensor and measurement method in the hardware documentation. |
| `ambient_c` | Ambient temperature in °C | Confirm sensor placement and calibration. |
| `humidity_pct` | Relative humidity (%) | Environmental reading. |
| `light_lux` | Illuminance (lux) | Ambient light level. |
| `co2_ppm` | CO₂ concentration (ppm) | Sensor-specific accuracy and calibration must be established. |
| `bpm` | Heart rate (beats/min) | Optional; may be `null`. |
| `spo2_pct` | Estimated oxygen saturation (%) | Optional; may be `null`; not a medical measurement. |
| `distance_cm` | Distance (cm) | Ultrasonic proximity estimate. |
| `mq2_raw` | MQ-2 raw ADC value | Raw sensor output, not a selective measurement of a named toxic gas. |
| `pir` | Motion indication | Boolean-like motion state. |

Example telemetry packet:

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

The exact sensor part numbers, wiring, ADC scaling, calibration data and operating limits should be added to `hardware/` when confirmed against the actual build.

## Communication

- STM32 UART4 TX: PA0.
- ESP32 bridge A UART receive: GPIO16 / RX2.
- Common ground between the STM32 and ESP32 A.
- UART configuration: 115200 baud, 8 data bits, no parity, 1 stop bit (8N1).
- ESP32 A to ESP32 B: ESP-NOW.
- ESP32 B to host: USB serial; the documented Windows setup used COM28 at 115200 baud.

The browser does not communicate directly with the STM32 or ESP-NOW. The Python host process receives serial data and exposes it to the browser.

## Dashboard

The host application is `smartfire_x_digital_twin.py`. It uses:

- Python 3 for the host application and serial processing.
- `pyserial` for USB serial input.
- Python's built-in HTTP server for local web delivery and the telemetry API.
- HTML and CSS for the dashboard and HUD layout.
- JavaScript for periodic API polling and UI updates.
- HTML canvas/SVG elements for selected charts and route-map illustration.

The documented local address is `http://127.0.0.1:8765`. The browser polls the local API approximately every 500 ms. This is a UI refresh interval, not a measured end-to-end sensor latency.

## Risk intelligence and diagnostics

`risk_engine.py` implements a transparent rule-based prototype. It uses configured thresholds, selected combinations and recent trends to generate a score/category and explanatory evidence. The displayed categories are:

- NORMAL
- GUARDED
- HIGH
- CRITICAL

Evidence coverage indicates how many expected inputs are available; it is not a probability of danger. The thresholds are prototype settings and must not be represented as certified exposure limits.

The MQ-2 channel is treated as a raw ADC signal. It cannot, by itself, identify a specific toxic gas. A CO₂ threshold or MQ-2 raw threshold in the visor is a prototype alert condition, not proof of a toxic atmosphere.

## 3D digital twin and visor HUD

The browser-based scene is built with Three.js and includes a schematic multi-room building, floors/partitions, camera controls, an avatar image plane, and a fixed route illustration.

The visor mode changes the camera presentation to a first-person-style view, hides the avatar, and displays selected live telemetry and alert cues. A red alert cue is configured for CO₂ >= 1500 ppm or MQ-2 raw ADC >= 1200.

**Current limitations:**
- The building is schematic, not a surveyed floor plan, CAD/BIM model or complete physical replica.
- The route is predefined and illustrative; it is not dynamically planned.
- There is no validated real-time firefighter localization, obstacle mapping or route replanning.
- The HUD is rendered in a browser, not projected onto a physical optical visor or smart-glasses display.
- The avatar is a textured image plane, not a fully rigged 3D character.

## Repository layout

```text
hardware/       Sensor, wiring, pinout and communication documentation
software/       Python application, risk engine and embedded reference logic
docs/           Project report, diary, architecture and test documentation
assets/         Dashboard, digital-twin and helmet integration images
examples/       Example telemetry packets and test data
```

Image locations and naming guidance are in [docs/IMAGE_GUIDE.md](docs/IMAGE_GUIDE.md).

## Setup

### Requirements

- Python 3.10 or later recommended.
- Windows/Linux host.
- USB connection to ESP32 bridge B.
- Three.js is currently loaded by the browser from a CDN, so an internet connection may be required unless the library is bundled locally.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Run

1. Power the STM32 and both ESP32 boards.
2. Connect ESP32 bridge B to the host computer.
3. Close any serial monitor already using the receiver port.
4. Update the serial port in the application if it differs from COM28.
5. From the project directory, run:

```bash
python smartfire_x_digital_twin.py
```

6. Open `http://127.0.0.1:8765` in a browser.

On Linux, the serial device may appear as `/dev/ttyUSB0` or `/dev/ttyACM0`; use the actual device shown by the operating system.

## Validation status

The packaged application source was syntax-checked during development. That check does not establish full runtime compatibility, sensor accuracy, wireless reliability, safety performance or real-world navigation capability. Record repeatable test procedures and measured results in `docs/TESTING.md`.

## Roadmap

- [ ] Add verified sensor part numbers, wiring diagrams and calibration notes.
- [ ] Add real dashboard and digital-twin screenshots to `assets/`.
- [ ] Add helmet sensor-placement photographs/illustrations.
- [ ] Record UART/ESP-NOW packet format, timing and error handling.
- [ ] Measure packet loss, wireless range and end-to-end latency.
- [ ] Add automated tests for JSON parsing and risk rules.
- [ ] Replace schematic floor plan with a mapped building model.
- [ ] Implement and validate localization and dynamic route planning.
- [ ] Evaluate physical visor/display integration.
- [ ] Conduct safety and domain validation before any operational use.

## Author

**Vamsi Krishna Theegela**  
Electronics Engineering (VLSI), Manipal Institute of Technology

## License

This repository is intended for academic and demonstration use. See [LICENSE](LICENSE).
