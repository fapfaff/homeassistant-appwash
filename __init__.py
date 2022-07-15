"""The AppWash integration."""
from __future__ import annotations

from appwashpy import AppWash

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_LOCATION, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AppWash from a config entry."""

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    location = entry.data[CONF_LOCATION]

    # hass.data[DOMAIN][entry.entry_id] = AppWash(email, password, location)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = AppWash(
        email, password, location
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
