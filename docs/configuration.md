# Configuration

Start Time has no options. Once added, it creates a single `sensor.start_time`
entity.

## UI

Settings → Devices & Services → **Add Integration** → **Start Time**.

## YAML (legacy)

```yaml
start_time:
```

Only a single instance is supported.

## Entity

- **State**: boot initialization time, in seconds.
- **Attributes**: per-integration setup durations, sorted slowest first.
