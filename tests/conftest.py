"""Shared fixtures for the Start Time test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from custom_components.start_time.const import DOMAIN
from pytest_homeassistant_custom_component.common import MockConfigEntry

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable loading custom integrations in all tests."""


@pytest.fixture
def config_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Return a Start Time config entry added to hass."""
    entry = MockConfigEntry(domain=DOMAIN, title="Start Time", data={})
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
async def setup_integration(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the Start Time integration and return the loaded entry."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
