"""The Start Time integration.

Exposes the Home Assistant boot duration as a sensor, with per-integration
setup times as attributes. Config-entry only; a single instance is allowed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .boot import BootTimeMonitor

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

PLATFORMS: Final = [Platform.SENSOR]

type StartTimeConfigEntry = ConfigEntry[BootTimeMonitor]


async def async_setup_entry(hass: HomeAssistant, entry: StartTimeConfigEntry) -> bool:
    """Set up Start Time from a config entry."""
    monitor = BootTimeMonitor()
    monitor.attach()
    entry.async_on_unload(monitor.detach)
    entry.runtime_data = monitor

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: StartTimeConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
