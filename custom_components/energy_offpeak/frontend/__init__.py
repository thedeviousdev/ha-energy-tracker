"""Lovelace frontend registration for Energy Window Tracker."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from ..const import URL_BASE

_LOGGER = logging.getLogger(__name__)


class JSModuleRegistration:
    """Register static path so the Lovelace card script is served."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def async_register(self) -> None:
        """Register static path for frontend files."""
        await self._async_register_path()

    async def _async_register_path(self) -> None:
        """Serve frontend files under URL_BASE."""
        try:
            await self.hass.http.async_register_static_paths(
                [StaticPathConfig(URL_BASE, Path(__file__).parent, False)]
            )
            _LOGGER.debug("Registered path %s", URL_BASE)
        except RuntimeError:
            _LOGGER.debug("Path %s already registered", URL_BASE)
