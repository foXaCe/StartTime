"""Tests for the Start Time diagnostics."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from custom_components.start_time.const import BOOTSTRAP_LOGGER_NAME
from custom_components.start_time.diagnostics import (
    async_get_config_entry_diagnostics,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_diagnostics_before_capture(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Diagnostics expose a null boot time before capture and real timings."""
    result = await async_get_config_entry_diagnostics(hass, setup_integration)
    assert result["boot_time"] is None
    assert isinstance(result["setup_timings"], dict)


async def test_diagnostics_after_capture(
    hass: HomeAssistant, setup_integration: MockConfigEntry
) -> None:
    """Diagnostics expose the captured boot time."""
    logging.getLogger(BOOTSTRAP_LOGGER_NAME).info(
        "Home Assistant initialized in %.2fs", 33.333
    )
    await hass.async_block_till_done()

    result = await async_get_config_entry_diagnostics(hass, setup_integration)
    assert result["boot_time"] == 33.33
