"""Sensor platform for the Start Time integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.setup import async_get_setup_timings

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import StartTimeConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: StartTimeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Start Time sensor from a config entry."""
    async_add_entities([StartTimeSensor(entry)])


class StartTimeSensor(Entity):
    """Sensor exposing the Home Assistant boot duration in seconds."""

    _attr_icon = "mdi:home-assistant"
    _attr_name = "Start Time"
    _attr_should_poll = False
    _attr_unique_id = DOMAIN
    _attr_unit_of_measurement = "seconds"

    def __init__(self, entry: StartTimeConfigEntry) -> None:
        """Initialize the sensor bound to the boot time monitor."""
        self._monitor = entry.runtime_data

    async def async_added_to_hass(self) -> None:
        """Subscribe to boot time capture; apply it if already available."""
        self.async_on_remove(self._monitor.add_listener(self._handle_boot_time))
        if self._monitor.boot_time is not None:
            self._apply_boot_time(self._monitor.boot_time)

    @callback
    def _handle_boot_time(self, boot_time: float) -> None:
        """Handle the boot time captured by the monitor."""
        self._apply_boot_time(boot_time)
        self.schedule_update_ha_state()

    def _apply_boot_time(self, boot_time: float) -> None:
        """Set the sensor state and per-integration setup time attributes."""
        self._attr_state = boot_time
        timings = async_get_setup_timings(self.hass)
        self._attr_extra_state_attributes = dict(
            sorted(
                ((domain, round(seconds, 2)) for domain, seconds in timings.items()),
                key=lambda item: item[1],
                reverse=True,
            )
        )
