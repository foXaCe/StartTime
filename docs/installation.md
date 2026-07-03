# Installation

## HACS (recommended)

1. Open HACS in Home Assistant.
2. Menu (top-right) → **Custom repositories**.
3. Add `foXaCe/StartTime` with category **Integration**.
4. Search for **Start Time** and install it.
5. Restart Home Assistant.

## Manual

1. Copy `custom_components/start_time/` into `<config>/custom_components/`.
2. Restart Home Assistant.

## Add the integration

Settings → Devices & Services → **Add Integration** → **Start Time**.

## Removal

1. Settings → Devices & Services → **Start Time** → entry menu → **Delete**.
2. In HACS, open **Start Time** → **Remove** (manual install: delete
   `custom_components/start_time/`).
3. Restart Home Assistant.

No leftover data remains: the integration has no options, no external
connections, and its stored state is removed with the entity.
