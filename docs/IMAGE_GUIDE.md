# Image Placement Guide

Add your own project images to the paths below. Keep image files in `assets/` and use short, descriptive filenames. Prefer PNG for screenshots/diagrams and JPG for photographs.

## Recommended images

| Image | Recommended filename | Where to use it |
|---|---|---|
| Dashboard full-screen screenshot | `assets/dashboard_overview.png` | README dashboard section |
| Digital twin building overview | `assets/digital_twin_overview.png` | README digital-twin section |
| Visor/HUD screenshot | `assets/visor_hud.png` | README visor section |
| Helmet with sensor placement | `assets/helmet_sensor_integration.png` | Hardware section |
| Full system architecture diagram | `assets/system_architecture.png` | README architecture section |
| STM32 and ESP32 hardware photograph | `assets/controller_communication_hardware.jpg` | Hardware documentation |
| Sensor close-up / wiring photograph | `assets/sensor_wiring.jpg` | Hardware documentation |

## How to add them

1. Open the repository on GitHub.
2. Open the `assets` folder.
3. Choose **Add file → Upload files**.
4. Drag the image files into the upload area.
5. Commit the changes to the `main` branch.

## Embed images in README

After uploading, add Markdown such as:

```markdown
![SMARTFIRE-X dashboard](assets/dashboard_overview.png)
```

Use relative paths exactly as shown. Do not upload images containing private credentials, personal data, serial numbers that should remain private, or identifiable people without permission.
