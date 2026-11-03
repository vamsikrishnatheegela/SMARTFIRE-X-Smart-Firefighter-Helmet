# Hardware Documentation

Document the final physical build here.

## Known controller and communication details

- Main controller board: STM32L4S5VIT6 on B-L4S5I-IOT01A.
- UART TX: STM32 PA0 / UART4_TX.
- ESP32 bridge A UART RX: GPIO16 / RX2.
- UART: 115200 baud, 8N1.
- Common ground between STM32 and ESP32 A.
- Wireless bridge: ESP-NOW from ESP32 A to ESP32 B.
- Host link: ESP32 B over USB serial (documented Windows port COM28).

## Sensor inventory to complete

For each sensor, add exact manufacturer/model, supply voltage, interface, pin mapping, range, accuracy, calibration method and mounting location.

- Temperature / object temperature
- Ambient temperature
- Relative humidity
- Light / illuminance
- CO₂
- MQ-2 gas-sensor module (raw ADC)
- PIR motion
- Ultrasonic distance
- Optional pulse-rate / SpO₂ sensor

Do not infer exact part numbers from telemetry keys. Add a wiring diagram and clear photographs when available.
