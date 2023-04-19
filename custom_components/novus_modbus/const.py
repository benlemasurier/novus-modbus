from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntityDescription,
)

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
class NovusRegister:
    """Describes Novus controller values"""


@dataclass
class NovusNumber(NovusRegister, NumberEntityDescription):
    """Represents Novus Number Values"""


@dataclass
class NovusBinarySensor(NovusRegister, BinarySensorEntityDescription):
    """Represents Novus Binary Sensors"""


class NovusPowerStatus(NovusBinarySensor):
    """Novus Power Status"""
    device_class = BinarySensorDeviceClass.POWER


@dataclass
class NovusTemperature(NovusRegister, SensorEntityDescription):
    """A class describing Novus temperature registers"""

    state_class = (STATE_CLASS_MEASUREMENT,)
    device_class = (SensorDeviceClass.TEMPERATURE,)
    native_unit_of_measurement = (TEMP_CELSIUS,)
    entity_registry_enabled_default = (True,)


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
    "r3": NovusTemperature(
        key="don",
        name="Differential setpoint for pump activation (dOn)",
    ),
    "r4": NovusTemperature(
        key="doff",
        name="Differential setpoint for pump deactivation (dOff)",
    ),
    "r5": NovusTemperature(
        key="ind",
        name="Temperature value shown on display (Ind)",
    ),
    "r6": NovusNumber(
        key="serial_high",
        name="First 3 digits of the controller serial number",
    ),
    "r7": NovusNumber(
        key="serial_low",
        name="Last 3 digits of the controller serial number",
    ),
    "r8": NovusTemperature(
        key="ice",
        name="Anti-frost temperature setpoint (ICE)",
    ),
    "r9": NovusTemperature(
        key="ht1",
        name="Temperature setpoint T1 overheating (Ht1)",
    ),
    "r10": NovusTemperature(
        key="ht2",
        name="Temperature setpoint T2 critical maximum in the tank (Ht2)",
    ),
    "r11": NovusTemperature(
        key="hys",
        name="Anti-frost temperature T1 hysteresis (HYS)",
    ),
    "r12": NovusTemperature(
        key="hy1",
        name="Hysteresis of the overheating temperature T1 (Hy1)",
    ),
    "r13": NovusTemperature(
        key="hy2",
        name="Hysteresis of the overheating temperature T2 (Hy2)",
    ),
    "r14": NovusNumber(
        key="ihm",
        name="FIXME IHM status bits",
    ),
    "r15": NovusNumber(
        key="control_status",
        name="Measurement Status",
    ),
    "r16": NovusNumber(
        key="screen_display_value",
        name="Value displayed on screen",
    ),
    "r17": NovusNumber(
        key="version_and_screen_n",
        name="Software version and currently displayed screen",
    ),
    "r18": NovusTemperature(
        key="of1",
        name="Offset value for sensor 1 measurement (oF1)",
    ),
    "r19": NovusTemperature(
        key="of2",
        name="Offset value for sensor 2 measurement (oF2)",
    ),
    "r20": NovusNumber(
        key="ice_ht1_ht2_status",
        name="FIXME: ICE, HT1, and HT2 status bits",
    ),
    "ihm_p1_out1": NovusPowerStatus(
        key="ihm_p1_out1",
        name="P1 (OUT1) Status",
    ),
    "ihm_p2_out2": NovusPowerStatus(
        key="ihm_p2_out2",
        name="P2 (OUT2) Status",
    ),
}
