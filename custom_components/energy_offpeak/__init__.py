"""Energy Window Tracker integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, INTEGRATION_VERSION
from .frontend import JSModuleRegistration

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/version"})
@websocket_api.async_response
async def _ws_version(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Handle version request from frontend."""
    connection.send_result(msg["id"], {"version": INTEGRATION_VERSION})


async def _async_register_frontend(hass: HomeAssistant) -> None:
    """Register Lovelace static path and resources (once per integration)."""
    registrar = JSModuleRegistration(hass)
    await registrar.async_register()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energy Window Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    if "frontend_registered" not in hass.data[DOMAIN]:
        websocket_api.async_register_command(hass, _ws_version)
        await _async_register_frontend(hass)
        hass.data[DOMAIN]["frontend_registered"] = True
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)
