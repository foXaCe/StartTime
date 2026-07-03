# Start Time for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![CI][ci-shield]][ci]
[![hassfest][hassfest-shield]][hassfest]
[![Maintenance][maintenance-shield]][maintenance]

_Custom Home Assistant integration that exposes Home Assistant's boot
initialization time as a sensor._

![sensor](sensor.png)

## Features

- **Start Time** sensor reporting the boot time in seconds — the same value
  Home Assistant logs at startup (`Home Assistant initialized in 25.5s`).
- Per-integration setup durations exposed as attributes, sorted from slowest to
  fastest — handy to spot what slows your startup down.
- Works independently of the `logger` component settings.

## Requirements

- Home Assistant >= 2024.4
- Python >= 3.13

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Menu (top-right) → **Custom repositories**.
3. Add `foXaCe/StartTime` with category **Integration**.
4. Search for **Start Time** and install it.
5. Restart Home Assistant.
6. Settings → Devices & Services → **Add Integration** → **Start Time**.

### Manual

1. Copy `custom_components/start_time/` into your `<config>/custom_components/`
   folder.
2. Restart Home Assistant.
3. Add the integration from the UI.

## Configuration

Settings → Devices & Services → **Add Integration** → **Start Time**.

If the integration is not in the list, clear the browser cache.

## About

Home Assistant reports its initialization time in the `INFO` logs. This
component surfaces the same value as a sensor:

```
2020-02-24 17:13:11 INFO (MainThread) [homeassistant.bootstrap] Home Assistant initialized in 25.5s
```

Useful for debugging startup performance on slow hardware such as a Raspberry Pi.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — this is a maintained fork of
[AlexxIT/StartTime](https://github.com/AlexxIT/StartTime).

<!-- Badges -->
[releases-shield]: https://img.shields.io/github/v/release/foXaCe/StartTime?style=for-the-badge
[releases]: https://github.com/foXaCe/StartTime/releases
[license-shield]: https://img.shields.io/github/license/foXaCe/StartTime?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[ci-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/StartTime/ci.yml?branch=main&style=for-the-badge&label=CI
[ci]: https://github.com/foXaCe/StartTime/actions/workflows/ci.yml
[hassfest-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/StartTime/hassfest.yml?branch=main&style=for-the-badge&label=hassfest
[hassfest]: https://github.com/foXaCe/StartTime/actions/workflows/hassfest.yml
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg?style=for-the-badge
[maintenance]: https://github.com/foXaCe/StartTime/commits/main
