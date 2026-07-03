# Start Time

Creates a **Start Time** sensor for Home Assistant that reports the boot
initialization time — the same value Home Assistant logs at startup:

```
Home Assistant initialized in 25.5s
```

The sensor also exposes per-integration setup durations as attributes, sorted
from slowest to fastest. Useful for debugging startup performance on slow
hardware such as a Raspberry Pi.

## Configuration

Settings → Devices & Services → Add Integration → **Start Time**
