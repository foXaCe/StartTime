# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0](https://github.com/foXaCe/StartTime/compare/v1.2.0...v1.3.0) (2026-07-03)


### Added

* reach Quality Scale Platinum (parallel-updates, icon translations, docs, strict typing) ([9a19e1c](https://github.com/foXaCe/StartTime/commit/9a19e1c09c56536acb3b02da260448fdfd0a8a38))

## [Unreleased]

## [1.2.0] - 2026-07-03

### Changed

- **Full integration overhaul** to 2026 Home Assistant standards:
  - Boot time capture rewritten as a removable `logging.Filter`
    (`BootTimeMonitor`) — the previous `logger.info` monkey-patch is gone;
    the hook detaches itself as soon as the boot time is captured (zero
    residual cost) and is also cleanly detached on config entry unload.
  - Typed `ConfigEntry.runtime_data` replaces `hass.data[DOMAIN]` (no more
    leak on unload).
  - Setup timings now come from the public
    `homeassistant.setup.async_get_setup_timings()` helper instead of the
    private `hass.data["setup_time"]` (multi-version format handling removed).
  - Sensor modernised: `RestoreSensor`, `native_value`, duration device class,
    `s` unit, measurement state class, display precision, `has_entity_name`
    and a service device (manufacturer/model/version/configuration URL).
    `unique_id` is unchanged — existing history and automations are preserved.
  - The boot value is now restored across restarts: the sensor no longer stays
    `unknown` when the integration is added on an already-running instance.
  - Per-integration setup-timing attributes are excluded from recorder history
    to avoid database bloat (still available live and in diagnostics).
  - `integration_type` corrected from `helper` to `service` (the integration
    now appears on the Integrations dashboard) and `single_config_entry: true`
    added.
  - Minimum Home Assistant version raised to 2025.1.0.
- Repository modernised: CI, HACS/hassfest validation, Renovate, `release-please`
  release pipeline, pre-commit (prek), devcontainer and full documentation.

### Added

- Diagnostics support (boot time + per-integration setup timings dump).
- Behavioral test suite: 26 tests, 100% coverage
  (`pytest-homeassistant-custom-component`).

### Removed

- Legacy YAML configuration support (`start_time:` + import flow). Existing
  config entries are unaffected; the integration is configured via the UI.

## [1.1.8]

### Fixed

- Support for Home Assistant 2024.4 setup-time reporting.

[Unreleased]: https://github.com/foXaCe/StartTime/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/foXaCe/StartTime/releases/tag/v1.2.0
[1.1.8]: https://github.com/foXaCe/StartTime/releases/tag/v1.1.8
