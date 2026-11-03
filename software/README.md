# Software Components

The current host-side application package contains:

- `smartfire_x_digital_twin.py` — Python host application, serial ingestion, local web server and browser UI.
- `risk_engine.py` — rule-based risk scoring and evidence explanations.
- `risk_engine_demo.py` — standalone demonstration of risk-engine behaviour.
- `smartfire_edge_logic.c` / `.h` — reference C logic for possible future embedded implementation; not integrated into the existing STM32 firmware.

The browser interface uses HTML, CSS and JavaScript, with Three.js for the schematic 3D scene. Python uses pyserial for the USB serial receiver. See the root README for setup and architecture.
