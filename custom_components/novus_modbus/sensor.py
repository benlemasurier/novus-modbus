from __future__ import annotations

from datetime import datetime
import logging
from typing import Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import homeassistant.util.dt as dt_util

from .const import (
    ATTR_MANUFACTURER,
    DOMAIN,
    REGISTERS,
    NovusRegister,
)
from .hub import NovusModbusHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]

    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": hub_name,
        "manufacturer": ATTR_MANUFACTURER,
    }

    entities = []
    for item_description in REGISTERS.values():
        entity = NovusEntity(
            hub_name,
            hub,
            device_info,
            item_description,
        )
        entities.append(entity)

    async_add_entities(entities)
    return True


class NovusEntity(CoordinatorEntity,
                  SensorEntity,
                  BinarySensorEntity,
                  NumberEntity):
    """Novus modbus register entity"""

    def __init__(
        self,
        platform_name: str,
        hub: NovusModbusHub,
        device_info,
        description: NovusRegister,
    ):
        """Initialize the entity."""
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self.entity_description: NovusRegister = description

        super().__init__(coordinator=hub)

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the entity."""
        return (
            self.coordinator.data[self.entity_description.key]
            if self.entity_description.key in self.coordinator.data
            else None
        )
