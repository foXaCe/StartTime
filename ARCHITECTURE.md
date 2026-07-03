# Architecture

`start_time` is a minimal Home Assistant integration that surfaces Home
Assistant's own boot initialization time as a sensor entity.

## Flow

```
homeassistant.bootstrap logger
        │  "Home Assistant initialized in 25.5s"
        ▼
BootTimeMonitor (logging.Filter, attached at entry setup, self-detached
        │        right after capture — and on unload — never mutates
        │        logging behavior)
        │  captures the float argument, notifies listeners
        ▼
StartTimeSensor._handle_boot_time()
        │  reads homeassistant.setup.async_get_setup_timings(hass)  (public API)
        ▼
sensor.start_time  (native_value = seconds, attributes = per-integration
                    setup times sorted slowest-first, excluded from recorder)
```

## Components

| File | Responsibility |
|------|----------------|
| `__init__.py` | Config entry lifecycle only: creates the `BootTimeMonitor`, stores it in typed `entry.runtime_data` (`StartTimeConfigEntry`), forwards the sensor platform, detaches the monitor on unload (`entry.async_on_unload`). |
| `const.py` | `DOMAIN`, bootstrap logger name and boot message prefix. No logic, no HA imports. |
| `boot.py` | `BootTimeMonitor`, a standard `logging.Filter` attached to the `homeassistant.bootstrap` logger. Captures the boot duration from the log record arguments (first capture wins), notifies subscribed listeners, always lets records through. Pure `logging` — fully unit-testable without Home Assistant. |
| `config_flow.py` | Single-instance config flow, no user input. Duplicates are blocked by `single_config_entry: true` in the manifest (core-level). |
| `sensor.py` | Platform setup + `StartTimeSensor` (`RestoreSensor`): duration device class, seconds unit, measurement state class, service `DeviceInfo`. Subscribes to the monitor; if the entity is added after boot already completed, the previous value is restored so the sensor never stays unknown. Setup-timing attributes are excluded from recorder history (`_unrecorded_attributes`). |
| `diagnostics.py` | Config entry diagnostics: captured boot time + raw per-integration setup timings. |

## Data sources

- **Boot duration**: the argument of the `"Home Assistant initialized in %.2fs"`
  log record emitted by `homeassistant.bootstrap` at the end of startup. This is
  the exact number HA computes itself — the integration performs no timing of
  its own.
- **Per-integration setup times**: `homeassistant.setup.async_get_setup_timings()`
  (public helper, HA ≥ 2024.5), replacing the former private
  `hass.data["setup_time"]` access and its multi-version format handling.

## Design constraints

- **Zero boot cost**: no I/O, no polling, no third-party requirements. The only
  runtime hook is one `logging.Filter` on a logger that emits a handful of
  records per boot — and it detaches itself as soon as the capture is done
  (deferred outside the logging call, since a logger's filter list must not be
  mutated while logging iterates over it). Zero residual hook after boot.
- **unique_id stability**: the single entity keeps `unique_id = "start_time"`
  (unchanged since the original implementation — user history and automations
  are preserved).
- **Clean lifecycle**: the filter is detached and listeners cleared on entry
  unload; reloads never stack filters (covered by tests).

## Extension points

- **New platform**: create `<platform>.py` with `async_setup_entry`, add
  `Platform.<X>` to `PLATFORMS` in `__init__.py`, subscribe to
  `entry.runtime_data` (the `BootTimeMonitor`) for capture notifications.
- **New captured metric**: extend `BootTimeMonitor.filter()` (keep the
  first-capture-wins and always-pass-through invariants), expose through
  a new entity or attribute.

## Tests

`tests/` covers 100% of the integration: `test_boot.py` (pure unit tests of the
filter), `test_init.py` (lifecycle, no filter leak/stacking), `test_config_flow.py`
(creation + single-instance abort), `test_sensor.py` (capture, restore-on-add,
pre-add capture race, registry stability, metadata), `test_diagnostics.py`, and
`test_manifest.py` (structural JSON checks). Run with
`pytest` (needs `pytest-homeassistant-custom-component`, see
`requirements_test.txt`).
