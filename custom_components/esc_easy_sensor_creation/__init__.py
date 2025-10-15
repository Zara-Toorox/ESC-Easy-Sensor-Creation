"""ESC Easy Sensor Creation Integration."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ESC Easy Sensor Creation from a config entry."""
    device_registry = dr.async_get(hass)
    
    # Create a single, central device for the integration
    # All entities will be attached to this device.
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, DOMAIN)}, # Static identifier for the whole integration
        name="ESC Easy Sensor Creation",
        manufacturer="ESC by Zara Toorox",
        model="Sensor Creator",
        sw_version="5.0.3",
    )
    _LOGGER.debug(f"Zentrales ESC-Gerät sichergestellt.")
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    