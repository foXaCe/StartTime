"""Sensor platform for the Start Time integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import MATCH_ALL, UnitOfTime
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.loader import async_get_integration
from homeassistant.setup import async_get_setup_timings

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import StartTimeConfigEntry

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: StartTimeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Start Time sensor from a config entry."""
    integration = await async_get_integration(hass, DOMAIN)
    sw_version = str(integration.version) if integration.version else None
    async_add_entities([StartTimeSensor(entry, sw_version)])


class StartTimeSensor(RestoreSensor):
    """Sensor exposing the Home Assistant boot duration in seconds.

    The value comes from the :class:`~.boot.BootTimeMonitor` capture. When the
    entity is added after the boot message already fired (e.g. the integration
    was installed on a running instance), the previous value is restored so the
    sensor never stays unknown.
    """

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_has_entity_name = True
    _attr_name = None
    # Icon provided through icons.json (icon translations); the explicit
    # _attr_name = None keeps the device name as the entity name.
    _attr_translation_key = DOMAIN
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 2
    _attr_unique_id = DOMAIN
    # Per-integration setup timings change on every boot and would bloat the
    # recorder database; keep them out of history (still visible live).
    _unrecorded_attributes = frozenset({MATCH_ALL})

    def __init__(self, entry: StartTimeConfigEntry, sw_version: str | None) -> None:
        """Initialize the sensor bound to the boot time monitor."""
        self._monitor = entry.runtime_data
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Start Time",
            manufacturer="foXaCe",
            model="Home Assistant boot time",
            sw_version=sw_version,
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://github.com/foXaCe/StartTime",
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to boot capture, or restore the previous boot value."""
        await super().async_added_to_hass()
        self.async_on_remove(self._monitor.add_listener(self._handle_boot_time))
        if self._monitor.boot_time is not None:
            self._apply_boot_time(self._monitor.boot_time)
        elif (last_data := await self.async_get_last_sensor_data()) is not None:
            _LOGGER.debug("Restoring previous boot time: %s", last_data.native_value)
            self._attr_native_value = last_data.native_value
            if (last_state := await self.async_get_last_state()) is not None:
                self._attr_extra_state_attributes = {
                    domain: seconds
                    for domain, seconds in last_state.attributes.items()
                    if isinstance(seconds, (int, float))
                    and not isinstance(seconds, bool)
                }

    @callback
    def _handle_boot_time(self, boot_time: float) -> None:
        """Handle the boot time captured by the monitor."""
        self._apply_boot_time(boot_time)
        self.schedule_update_ha_state()

    def _apply_boot_time(self, boot_time: float) -> None:
        """Set the sensor value and per-integration setup time attributes."""
        self._attr_native_value = boot_time
        timings = async_get_setup_timings(self.hass)
        self._attr_extra_state_attributes = dict(
            sorted(
                ((domain, round(seconds, 2)) for domain, seconds in timings.items()),
                key=lambda item: item[1],
                reverse=True,
            )
        )
