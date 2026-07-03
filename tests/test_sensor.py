"""Tests for the Start Time sensor entity."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from unittest.mock import patch

from custom_components.start_time.const import BOOTSTRAP_LOGGER_NAME, DOMAIN
from homeassistant.core import State
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import (
    mock_restore_cache_with_extra_data,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry


def _fire_boot_message(seconds: float) -> None:
    """Emit the real bootstrap log record HA produces at end of startup."""
    logging.getLogger(BOOTSTRAP_LOGGER_NAME).info(
        "Home Assistant initialized in %.2fs", seconds
    )


async def test_boot_capture_updates_state_and_attributes(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """The sensor exposes the exact captured value with sorted timings."""
    with patch(
        "custom_components.start_time.sensor.async_get_setup_timings",
        return_value={"slow": 7.891, "fast": 0.123, "medium": 3.456},
    ):
        _fire_boot_message(25.184)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert float(state.state) == 25.18

    timings = {
        k: v for k, v in state.attributes.items() if k in ("slow", "medium", "fast")
    }
    assert timings == {"slow": 7.89, "medium": 3.46, "fast": 0.12}
    assert list(timings) == ["slow", "medium", "fast"]  # slowest first


async def test_restores_previous_value_when_boot_already_passed(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> None:
    """Added after boot: the previous value is restored, never unknown."""
    mock_restore_cache_with_extra_data(
        hass,
        (
            (
                State(
                    "sensor.start_time",
                    "20.5",
                    {"homeassistant": 1.23, "icon": "mdi:home-assistant"},
                ),
                {"native_value": 20.5, "native_unit_of_measurement": "s"},
            ),
        ),
    )

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert float(state.state) == 20.5
    # Numeric timing attributes restored, decorative strings filtered out.
    assert state.attributes["homeassistant"] == 1.23


async def test_capture_before_entity_is_added(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> None:
    """A capture landing before the entity exists is applied on add."""
    original = hass.config_entries.async_forward_entry_setups

    async def fire_then_forward(entry, platforms):  # noqa: ANN001, ANN202
        _fire_boot_message(9.876)
        await original(entry, platforms)

    with patch.object(
        hass.config_entries, "async_forward_entry_setups", fire_then_forward
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert float(state.state) == 9.88


async def test_registry_device_and_unique_id(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """unique_id is stable and the service device is fully described."""
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.start_time")
    assert entry is not None
    assert entry.unique_id == "start_time"
    assert entry.device_id is not None

    device_registry = dr.async_get(hass)
    device = device_registry.async_get(entry.device_id)
    assert device is not None
    assert device.identifiers == {(DOMAIN, setup_integration.entry_id)}
    assert device.entry_type is dr.DeviceEntryType.SERVICE
    assert device.manufacturer == "foXaCe"
    assert device.sw_version


async def test_sensor_metadata(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Device class, unit and state class follow the modern sensor model."""
    _fire_boot_message(11.0)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert state.attributes["device_class"] == "duration"
    assert state.attributes["unit_of_measurement"] == "s"
    assert state.attributes["state_class"] == "measurement"
