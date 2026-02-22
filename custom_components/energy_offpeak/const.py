"""Constants for the Energy Window Tracker integration."""

from pathlib import Path
import json

DOMAIN = "energy_offpeak"

# Read version from manifest for frontend sync
_MANIFEST_PATH = Path(__file__).parent / "manifest.json"
with open(_MANIFEST_PATH, encoding="utf-8") as _f:
    INTEGRATION_VERSION: str = json.load(_f).get("version", "0.0.0")

# Base URL for Lovelace card script
URL_BASE: str = "/energy-window-tracker"

CONF_SOURCE_ENTITY = "source_entity"
CONF_NAME = "name"
CONF_WINDOWS = "windows"
CONF_WINDOW_START = "start"
CONF_WINDOW_END = "end"
CONF_WINDOW_NAME = "name"

DEFAULT_NAME = "Window"
DEFAULT_WINDOW_START = "11:00"
DEFAULT_WINDOW_END = "14:00"

STORAGE_VERSION = 1
STORAGE_KEY = "energy_offpeak_snapshots"

ATTR_SOURCE_ENTITY = "source_entity"
ATTR_STATUS = "status"
