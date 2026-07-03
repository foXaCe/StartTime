"""Tests for the Start Time integration lifecycle."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from custom_components.start_time.boot import BootTimeMonitor
from custom_components.start_time.const import BOOTSTRAP_LOGGER_NAME
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_UNKNOWN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry


def _monitor_count() -> int:
    """Count BootTimeMonitor filters attached to the bootstrap logger."""
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    return sum(isinstance(f, BootTimeMonitor) for f in logger.filters)


async def test_setup_creates_entity_and_attaches_filter(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> None:
    """Setup loads the entry, exposes the sensor and attaches the filter."""
    baseline = _monitor_count()

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED
    assert isinstance(config_entry.runtime_data, BootTimeMonitor)
    assert _monitor_count() == baseline + 1

    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert state.state == STATE_UNKNOWN


async def test_unload_detaches_filter(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Unloading removes the logging filter — no leak."""
    attached = _monitor_count()

    assert await hass.config_entries.async_unload(setup_integration.entry_id)
    await hass.async_block_till_done()

    assert setup_integration.state is ConfigEntryState.NOT_LOADED
    assert _monitor_count() == attached - 1


async def test_filter_detaches_itself_after_capture(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Once the boot time is captured, the filter fully detaches itself."""
    attached = _monitor_count()

    logging.getLogger(BOOTSTRAP_LOGGER_NAME).info(
        "Home Assistant initialized in %.2fs", 8.0
    )
    await hass.async_block_till_done()

    assert _monitor_count() == attached - 1  # zero residual hook
    state = hass.states.get("sensor.start_time")
    assert state is not None
    assert float(state.state) == 8.0

    # Unload after self-detach stays clean (detach is idempotent).
    assert await hass.config_entries.async_unload(setup_integration.entry_id)
    await hass.async_block_till_done()
    assert setup_integration.state is ConfigEntryState.NOT_LOADED


async def test_reload_does_not_stack_filters(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Reloading the entry never stacks bootstrap logger filters."""
    attached = _monitor_count()

    assert await hass.config_entries.async_reload(setup_integration.entry_id)
    await hass.async_block_till_done()

    assert setup_integration.state is ConfigEntryState.LOADED
    assert _monitor_count() == attached
