"""Tests for the Start Time config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.start_time.const import DOMAIN
from homeassistant.config_entries import SOURCE_USER
from homeassistant.data_entry_flow import FlowResultType

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """The user flow creates the entry immediately (nothing to configure)."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Start Time"
    assert result["data"] == {}

    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1


async def test_second_instance_aborts(
    hass: HomeAssistant, config_entry: MockConfigEntry
) -> None:
    """A second flow aborts: only a single instance is allowed."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
