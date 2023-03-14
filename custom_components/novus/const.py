from dataclasses import dataclass

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorDeviceClass,
    SensorEntityDescription,
)

from homeassistant.const import (
    TEMP_CELSIUS,
)

DOMAIN = "novus_modbus"
DEFAULT_NAME = "Novus Temperature Controller"
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_PORT = 502
ATTR_MANUFACTURER = "Novus Automation"


@dataclass
class NovusRegister(SensorEntityDescription):
    """A class that describes Novus controller registers"""


@dataclass
class NovusTemperature(NovusRegister):
    """A class describing Novus temperature registers"""
    state_class = STATE_CLASS_MEASUREMENT,
    device_class = SensorDeviceClass.TEMPERATURE,
    native_unit_of_measurement = TEMP_CELSIUS,
    entity_registry_enabled_default = True,


REGISTERS: dict[str, list[NovusRegister]] = {
    "r0": NovusTemperature(
        key="t1_temp_c",
        name="T1 Temperature",
        icon="mdi:thermometer",
    ),
    "r1": NovusTemperature(
        key="t2_temp_c",
        name="T2 Temperature",
        icon="mdi:thermometer",
    ),
    "r2": NovusTemperature(
        key="temp_diff_c",
        name="T1-T2 Temperature (dIF)",
        icon="mdi:thermometer",
    ),
    # "r3": NovusTemperature(
    #     key="diff_setpoint_c_on",
    #     name="Differential setpoint for pump activation (dOn)",
    # ),
    # "r4": NovusTemperature(
    #     key="diff_setpoint_c_off",
    #     name="Differential setpoint for pump deactivation (dOff)",
    # ),
    # # TODO:
    # # "r5": NovusRegister(
    # #     key="display_temp_cfg",
    # #     name="Temperature value shown on display (Ind)",
    # #     state_class=STATE_CLASS_MEASUREMENT,
    # #     native_unit_of_measurement=TEMP_CELSIUS,
    # #     device_class=SensorDeviceClass.TEMPERATURE,
    # #     entity_registry_enabled_default=True,
    # # ),
}
