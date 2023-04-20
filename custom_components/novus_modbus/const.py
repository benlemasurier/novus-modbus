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
    """Generic container for register values"""


@dataclass
class NovusTemperature(NovusRegister):
    """Registers holding temperature values"""

    state_class = (STATE_CLASS_MEASUREMENT,)
    device_class = (SensorDeviceClass.TEMPERATURE,)
    native_unit_of_measurement = (TEMP_CELSIUS,)
    entity_registry_enabled_default = (True,)
    icon = "mdi:thermometer"


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
    "r6": NovusRegister(
        key="serial_high",
        name="First 3 digits of the controller serial number",
    ),
    "r7": NovusRegister(
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
    # r14: IHM status bits (see below)
    "r15": NovusRegister(
        key="control_status",
        name="Measurement Status",
    ),
    "r16": NovusRegister(
        key="screen_display_value",
        name="Value displayed on screen",
    ),
    "r17": NovusRegister(
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
    # r20: ICE, HT1, HT2 status bits (see below)
    "ihm_p1_out1": NovusRegister(
        key="ihm_p1_out1",
        name="P1 (OUT1) Enabled",
    ),
    "ihm_p2_out2": NovusRegister(
        key="ihm_p2_out2",
        name="P2 (OUT2) Enabled",
    ),
    "ihm_pv": NovusRegister(
        key="ihm_pv",
        name="PV Enabled",
    ),
    "ihm_rx": NovusRegister(
        key="ihm_rx",
        name="Serial Command Received",
    ),
    "ihm_internal_4": NovusRegister(
        key="ihm_internal_4",
        name="Internal Control (bit 4)",
    ),
    "ihm_status_t1": NovusRegister(
        key="ihm_status_t1",
        name="T1 Status LED",
    ),
    "ihm_status_defrost": NovusRegister(
        key="ihm_status_defrost",
        name="Defrosting",
    ),
    "ihm_status_t2": NovusRegister(
        key="ihm_status_t2",
        name="T2 Status LED",
    ),
    "ihm_internal_8": NovusRegister(
        key="ihm_internal_8",
        name="Internal Control (bit 8)",
    ),
    "ihm_internal_9": NovusRegister(
        key="ihm_internal_9",
        name="Internal Control (bit 9)",
    ),
    "ihm_value_has_decimal": NovusRegister(
        key="ihm_value_has_decimal",
        name="Value has a decimal point",
    ),
    "ihm_internal_11": NovusRegister(
        key="ihm_internal_11",
        name="Internal Control (bit 11)",
    ),
    "ihm_internal_12": NovusRegister(
        key="ihm_internal_12",
        name="Internal Control (bit 12)",
    ),
    "ihm_internal_13": NovusRegister(
        key="ihm_internal_13",
        name="Internal Control (bit 13)",
    ),
    "ihm_internal_14": NovusRegister(
        key="ihm_internal_14",
        name="Internal Control (bit 14)",
    ),
    "ihm_internal_15": NovusRegister(
        key="ihm_internal_15",
        name="Internal Control (bit 15)",
    ),
    "ice_status": NovusRegister(
        key="ice_status",
        name="Defrosting Enabled (ICE)",
    ),
    "ht1_status": NovusRegister(
        key="ht1_status",
        name="HT1 Enabled",
    ),
    "ht2_status": NovusRegister(
        key="ht2_status",
        name="HT2 Enabled",
    ),
    # r21-23 (sp1, b1y, ac1) result in errors when read.
    # the documentation is very unclear here.
}
