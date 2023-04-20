"""Novus Modbus Hub"""
from datetime import timedelta
import logging
import threading
import pymodbus
from urllib.parse import urlparse

from homeassistant.core import CALLBACK_TYPE, callback
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.register_read_message import ReadHoldingRegistersResponse
from voluptuous.validators import Number

_LOGGER = logging.getLogger(__name__)


class NovusModbusHub(DataUpdateCoordinator[dict]):
    """Thread-safe data retrieval from a Novus Controller"""

    def __init__(
        self,
        hass: HomeAssistantType,
        name: str,
        hostname: str,
        scan_interval: Number,
    ):
        """Initialize the modbus hub."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=scan_interval),
        )

        # split the configured hostname into its component parts.
        # If it's not a URL it might be a serial port.
        # This logic is tested to work with linux and windows serial port names.
        parsed = urlparse(f"//{hostname}")
        if (parsed.port is None) and (
            (parsed.hostname is None) or (parsed.hostname[0:3] == "com")
        ):
            self._client = ModbusSerialClient(
                method="rtu",
                port=parsed.path + parsed.netloc,
                baudrate=9600,
                stopbits=1,
                bytesize=8,
                timeout=5,
            )
        else:
            if parsed.port is None:
                localport = 502
            else:
                localport = parsed.port

            self._client = ModbusTcpClient(
                host=parsed.hostname, port=localport, timeout=5
            )

        self._lock = threading.Lock()
        self.data: dict = {}

    @callback
    def async_remove_listener(self, update_callback: CALLBACK_TYPE) -> None:
        """Remove data update listener."""
        super().async_remove_listener(update_callback)

        """No listeners left then close connection"""
        if not self._listeners:
            self.close()

    def close(self) -> None:
        """Disconnect client."""
        with self._lock:
            self._client.close()

    def _read(self, unit, address, count) -> ReadHoldingRegistersResponse:
        """Read modbus holding registers"""

        with self._lock:
            kwargs = {"slave": unit}

            return self._client.read_holding_registers(address, count, **kwargs)

    async def _async_update_data(self) -> dict:
        realtime_data = {}
        try:
            realtime_data = await self.hass.async_add_executor_job(
                self.read_modbus_realtime_data
            )
        except ConnectionException:
            _LOGGER.error("read failed: controller is unreachable.")

        return realtime_data

    def read_modbus_realtime_data(self) -> dict:
        data = {}

        # TODO: data can only be read 4 registers at a time,
        # abstract this out so we don't need to keep calling _read()
        resp = self._read(unit=1, address=0, count=4)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        data["t1_temp_c"] = decoder.decode_16bit_int() / 10
        data["t2_temp_c"] = decoder.decode_16bit_int() / 10
        data["temp_diff_c"] = decoder.decode_16bit_int() / 10
        data["don"] = decoder.decode_16bit_int() / 10

        resp = self._read(unit=1, address=4, count=4)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        data["doff"] = decoder.decode_16bit_int() / 10
        # FIXME: account for decimal values?
        data["ind"] = decoder.decode_16bit_int()
        # FIXME: combine this into a single value
        data["serial_high"] = decoder.decode_16bit_int()
        data["serial_low"] = decoder.decode_16bit_int()

        resp = self._read(unit=1, address=8, count=4)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        data["ice"] = decoder.decode_16bit_int() / 10
        data["ht1"] = decoder.decode_16bit_int() / 10
        data["ht2"] = decoder.decode_16bit_int() / 10
        data["hys"] = decoder.decode_16bit_int() / 10

        resp = self._read(unit=1, address=12, count=4)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        data["hy1"] = decoder.decode_16bit_int()
        data["hy2"] = decoder.decode_16bit_int()
        # FIXME: extract bit values
        data["ihm"] = decoder.decode_16bit_int()
        data["control_status"] = decoder.decode_16bit_int()

        resp = self._read(unit=1, address=16, count=4)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        # FIXME: divide when screen may contain decimal values
        data["screen_display_value"] = decoder.decode_16bit_int()
        # FIXME: extract both values
        data["version_and_screen_n"] = decoder.decode_16bit_int()
        data["of1"] = decoder.decode_16bit_int()
        data["of2"] = decoder.decode_16bit_int()

        resp = self._read(unit=1, address=20, count=1)
        if resp.isError():
            return {}
        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers, byteorder=Endian.Big, wordorder=Endian.Little
        )
        # FIXME: extract values
        data["ice_ht1_ht2_status"] = decoder.decode_16bit_int()

        # sp1, b1y, and ac1 cause errors when read

        return data
