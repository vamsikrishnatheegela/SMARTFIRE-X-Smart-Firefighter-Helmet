# Testing and Validation

This document separates checks performed during software development from validation that still needs to be carried out on the complete hardware system.

## Existing development checks

- The packaged Python application source was syntax-checked.
- The documented telemetry JSON schema was used by the host application.
- The UART and ESP-NOW topology was established as part of the prototype communication path.
- The dashboard and digital-twin package was prepared for local execution.

A syntax check only confirms that source code parses. It does not prove successful runtime operation or hardware performance.

## Tests to record

| Test | Procedure | Result / measurement |
|---|---|---|
| UART integrity | Send known packets over STM32-to-ESP32 UART | To be measured |
| ESP-NOW delivery | Send numbered packets and count received/missing packets | To be measured |
| Serial parsing | Test valid, malformed and partial JSON lines | To be recorded |
| Sensor calibration | Compare each sensor against a suitable reference | To be measured |
| Stale-data detection | Stop packet transmission and observe dashboard status | To be recorded |
| Risk rule behaviour | Test values below, at and above each configured threshold | To be recorded |
| Dashboard update interval | Timestamp packet arrival and browser rendering | To be measured |
| End-to-end latency | Timestamp acquisition and host display using a defined method | To be measured |
| Digital-twin interaction | Verify overview, camera controls and visor toggle | To be recorded |
| Route correctness | Compare mapped route with a verified building plan | Not implemented; future work |

## Safety note

Do not infer a safe atmosphere from missing data, low MQ-2 raw ADC values, or a NORMAL dashboard category. No field deployment or life-safety claim should be made without appropriate sensor validation, certified equipment and expert review.
