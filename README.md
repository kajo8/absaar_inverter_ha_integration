# Absaar Inverter Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant integration for Absaar EMS inverters and battery systems. This integration connects to the Absaar EMS cloud service (MINI-EMS is also supported) and provides real-time monitoring of your solar inverter system.

## Features

- **GUI Configuration**: Easy setup through Home Assistant's UI
- **Automatic Updates**: Polls data every 2 minutes to avoid API rate limits
- **Comprehensive Data**: Exposes all available inverter metrics
- **Battery Support**: Full support for Absaar battery systems
- **Device Registry**: Properly registers devices in Home Assistant
- **Proper Entity IDs**: Uses unique identifiers for all sensors

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Pewidot/absaar_inverter_ha_integration`
6. Select category "Integration"
7. Click "Add"
8. Search for "Absaar Inverter" in HACS
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/absaar_ems` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Prerequisites

Before configuring the integration, you need:
1. An account in the Absaar EMS App with your inverter added
   - [Android App](https://play.google.com/store/apps/details?id=com.hy.miniemse&hl=de)
   - [iOS App](https://apps.apple.com/gb/app/absaarems/id6477900092)
2. Your Absaar EMS username (not email) and password

### Setup via UI

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Absaar Inverter**
4. Enter your Absaar EMS username and password
5. Click **Submit**

The integration will automatically discover your stations and inverters and create all sensors.

### Legacy YAML Configuration (Deprecated)

The old YAML configuration method is no longer supported. Please use the UI configuration method above. If you have an existing YAML configuration, remove it from your `configuration.yaml` and reconfigure through the UI.


## Available Sensors

The integration creates the following sensors for each inverter/station:

### Station Sensors
- **Daily Power Generation** (kWh) - Total energy generated today
- **Total Power Generation** (kWh) - Lifetime energy generation

### Inverter Sensors
- **AC Power** (W) - Current AC output power
- **AC Voltage** (V) - AC output voltage
- **AC Frequency** (Hz) - AC frequency
- **AC Current** (A) - AC output current
- **PV1 Power** (W) - Solar panel string 1 power
- **PV1 Voltage** (V) - Solar panel string 1 voltage
- **PV1 Current** (A) - Solar panel string 1 current
- **PV2 Power** (W) - Solar panel string 2 power
- **PV2 Voltage** (V) - Solar panel string 2 voltage
- **PV2 Current** (A) - Solar panel string 2 current
- **Input Power** (W) - Total DC input power
- **Temperature** (°C) - Inverter temperature

Additional sensors may be available depending on your specific hardware configuration, including:
- Battery voltage, current, and power
- Load power
- Controller temperature

## Troubleshooting

### Integration not showing up

1. Make sure you've restarted Home Assistant after installation
2. Check the logs for any errors: **Settings** → **System** → **Logs**
3. Verify that the `custom_components/absaar_ems` folder is in the correct location

### Authentication fails

1. Verify your username (not email address) and password are correct
2. Try logging into the Absaar EMS mobile app to confirm your credentials
3. Check your internet connection
4. The API endpoint may be temporarily unavailable - try again later

### No data showing

1. Check that your inverter is online and communicating with the Absaar EMS cloud
2. Verify in the mobile app that data is being received
3. Check Home Assistant logs for any API errors

## Support

If you encounter any issues or have feature requests, please:
1. Check existing [issues](https://github.com/Pewidot/absaar_inverter_ha_integration/issues)
2. Create a new issue with detailed information about your problem

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## Credits

- Created by [@Pewidot](https://github.com/Pewidot)
- Refactored with modern Home Assistant best practices

## License

This project is provided as-is for use with Absaar EMS systems.


