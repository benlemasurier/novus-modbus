"""
Custom integration for Novus Automation temperature controllers.
"""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from datetime import timedelta

from .const import DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, DOMAIN
from .hub import NovusHub

# FIXME: use __package__?
_LOGGER = logging.getLogger(__name__)

NOVUS_MODBUS_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(
        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
    ): cv.positive_int,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: NOVUS_MODBUS_SCHEMA
    })
}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]


async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle configuration via the UI."""
    name = entry.data[CONF_NAME]
    host = entry.data[CONF_HOST]
    interval = timedelta(seconds=entry.data[CONF_SCAN_INTERVAL])

    _LOGGER.debug("setup %s.%s", DOMAIN, name)

    # create and register the hub
    hub = NovusHub(hass, name, host, interval)
    hass.data[DOMAIN][name] = {"hub": hub}

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Removes a configuration entry."""
    unloaded = all(
        await asyncio.gather(*[
            hass.config_entries.async_forward_entry_unload(entry, component)
            for component in PLATFORMS
        ])
    )

    if not unloaded:
        return False

    hass.data[DOMAIN].pop(entry.data["name"])
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a configuration entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
