# Architecture

`start_time` is a minimal Home Assistant integration that surfaces Home
Assistant's own boot initialization time as a sensor entity.

## Flow

```
homeassistant.bootstrap logger
        │  "Home Assistant initialized in 25.5s"
        ▼
StartTime.add_logger()  ──patches──►  logger.info wrapper
        │  intercepts the init message
        ▼
StartTime.internal_update(state)
        │  reads hass.data["setup_time"]
        ▼
sensor.start_time  (state = seconds, attributes = per-integration setup times)
```

## Components

| File | Responsibility |
|------|----------------|
| `__init__.py` | Sets up the domain, forwards the sensor platform, handles YAML import and config entry lifecycle. |
| `config_flow.py` | Single-instance config flow (UI + YAML import), no user input. |
| `sensor.py` | The `StartTime` entity. Wraps `homeassistant.bootstrap`'s logger to capture the initialization message, then exposes the boot time as state and per-integration setup durations as attributes. |

## Notes

- The entity does not poll (`_attr_should_poll = False`); it updates once, when
  Home Assistant reports it has finished initializing.
- Setup-time reporting shape changed across HA versions; `internal_update`
  handles the `dict` (2024.4+), `float` (2024.3) and `timedelta` (pre-2024.3)
  forms.
