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
    ),
    "r1": NovusTemperature(
        key="t2_temp_c",
        name="T2 Temperature",
    ),
    "r2": NovusTemperature(
        key="temp_diff_c",
        name="T1-T2 Temperature (dIF)",
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

# FAULT_MESSAGES = {
#     0b000000000000000000000000010000000: "F08 GFCI Relay Failure",
#     0b000000000000000000001000000000000: "F13 Grid Mode Changed",
#     0b000000000000000000010000000000000: "F14 DC Over Current",
#     0b000000000000000000100000000000000: "F15 Software AC Over Current",
#     0b000000000000000001000000000000000: "F16 GFCI Detection",
#     0b000000000000000100000000000000000: "F18 Hardware AC Over Current",
#     0b000000000000010000000000000000000: "F20 DC Over Current",
#     0b000000000001000000000000000000000: "F22 Emergency Stop",
#     0b000000000010000000000000000000000: "F23 GFCI Overcurrent",
#     0b000000000100000000000000000000000: "F24 DC Insulation (ISO)",
#     0b000000010000000000000000000000000: "F26 Bus Unbalance",
#     0b000010000000000000000000000000000: "F29 Paralleled System",
#     0b100000000000000000000000000000000: "F33 AC Over Current"
# }
