"""Diagnostics support for the Start Time integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.setup import async_get_setup_timings

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from . import StartTimeConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: StartTimeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "boot_time": entry.runtime_data.boot_time,
        "setup_timings": {
            domain: round(seconds, 4)
            for domain, seconds in async_get_setup_timings(hass).items()
        },
    }
