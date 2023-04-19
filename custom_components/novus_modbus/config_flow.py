import re
import validators

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, callback
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .const import DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL, DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST, default="localhost"): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)


@callback
def novus_modbus_entries(hass: HomeAssistant):
    """Return the hosts already configured."""
    return {
        entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN)
    }


class NovusModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Novus Modbus configflow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle initial configuration"""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            if self._host_config_exists(host):
                errors[CONF_HOST] = "already_configured"
            elif not validators.url(host):
                errors[CONF_HOST] = "invalid host"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    def _host_config_exists(self, host) -> bool:
        """Return True if configuration already exists"""
        if host in novus_modbus_entries(self.hass):
            return True
        return False
