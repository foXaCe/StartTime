# Configuration

Start Time has no options. Once added, it creates a single `sensor.start_time`
entity attached to a **Start Time** service device.

## UI

Settings → Devices & Services → **Add Integration** → **Start Time**.

Only a single instance is supported (adding a second one is blocked).

> YAML configuration (`start_time:`) was removed; the integration is set up
> exclusively from the UI. Existing installations are unaffected.

## Entity

- **State**: boot initialization time, in seconds (duration device class).
  The value is the exact number Home Assistant logs as
  `Home Assistant initialized in X.XXs`.
- **Attributes**: per-integration setup durations, sorted slowest first.
  These attributes are not recorded in history to keep the database lean;
  they are always available live and in the integration diagnostics.
- The last value is restored after a restart until the new boot time is
  captured, so the sensor never stays `unknown`.
