[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
# AppWash
The `appwash` integration adds support for devices that can be used via Miele AppWash.
It offers a sensor for the state of the device.
Furthermore it adds the services `appwash.buy_service` and `appwash.stop_service` which will buy/start or stop the device.

## Installation
### Manual Installation
1. Download the
   [latest release](https://github.com/fapfaff/homeassistant-appwash/releases/latest).
2. Create a folder named `appwash` `custom_components` directory of your Home Assistant
   installation.
3. Unpack the release in the created directory.
4. Restart Home Assistant.

### Installation via HACS
1. Ensure that [HACS](https://custom-components.github.io/hacs/) is installed.
2. Add this repository as custom repository
3. Search for AppWash and install it!
4. Restart Home Assistant.

## Configuration

1. Login at [appwash.com](https://appwash.com/en/) to see your location id in the URL. For example *12345* for h<span>ttps://</span>appwash.com/myappwash/location/?id=*12345*
2. Add the integration to your Home Assistant.
3. Enter your AppWash Email and Password and the Location ID.
