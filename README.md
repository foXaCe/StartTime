# Start Time for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![HACS Custom][hacsbadge]][hacs]

[![CI][ci-shield]][ci]
[![Hassfest][hassfest-shield]][hassfest]
[![HACS validation][hacs-validation-shield]][hacs-validation]
[![Maintained][maintenance-shield]][maintenance]
[![Maintainer][maintainer-shield]][maintainer]

_A custom Home Assistant integration that exposes Home Assistant's own boot
initialization time as a sensor._

![Start Time sensor](sensor.png)

## Features

- A **Start Time** sensor reporting the boot time in seconds — the same value
  Home Assistant logs at startup (`Home Assistant initialized in 25.5s`).
- Per-integration setup durations exposed as sensor attributes, sorted from
  slowest to fastest — handy for spotting what slows your startup down.
- Works independently of your `logger` component settings.

## Requirements

- Home Assistant **2024.4** or newer
- Python **3.13** or newer

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Open the menu (top-right) → **Custom repositories**.
3. Add `foXaCe/StartTime` with the category **Integration**.
4. Search for **Start Time** and install it.
5. Restart Home Assistant.
6. Go to **Settings → Devices & Services → Add Integration → Start Time**.

### Manual

1. Copy the `custom_components/start_time/` folder into your
   `<config>/custom_components/` folder.
2. Restart Home Assistant.
3. Add the integration from the UI.

## Configuration

Go to **Settings → Devices & Services → Add Integration → Start Time**.

There is nothing to configure. If the integration does not appear in the list,
clear your browser cache and try again.

### The sensor

- **State**: the boot initialization time, in seconds.
- **Attributes**: per-integration setup durations, sorted slowest first.

## How it works

Home Assistant reports its initialization time in the `INFO` logs. This
integration surfaces the same value as a sensor:

```
2020-02-24 17:13:11 INFO (MainThread) [homeassistant.bootstrap] Home Assistant initialized in 25.5s
```

This is useful for debugging startup performance on slow hardware such as a
Raspberry Pi.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE). This is a maintained fork of
[AlexxIT/StartTime](https://github.com/AlexxIT/StartTime).

<!-- Badges -->
[releases-shield]: https://img.shields.io/github/v/release/foXaCe/StartTime?style=for-the-badge
[releases]: https://github.com/foXaCe/StartTime/releases
[license-shield]: https://img.shields.io/github/license/foXaCe/StartTime?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[ci-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/StartTime/ci.yml?branch=main&style=for-the-badge&label=CI
[ci]: https://github.com/foXaCe/StartTime/actions/workflows/ci.yml
[hassfest-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/StartTime/hassfest.yml?branch=main&style=for-the-badge&label=Hassfest
[hassfest]: https://github.com/foXaCe/StartTime/actions/workflows/hassfest.yml
[hacs-validation-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/StartTime/hacs.yml?branch=main&style=for-the-badge&label=HACS
[hacs-validation]: https://github.com/foXaCe/StartTime/actions/workflows/hacs.yml
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg?style=for-the-badge
[maintenance]: https://github.com/foXaCe/StartTime/commits/main
[maintainer-shield]: https://img.shields.io/badge/maintainer-%40foXaCe-blue.svg?style=for-the-badge
[maintainer]: https://github.com/foXaCe
