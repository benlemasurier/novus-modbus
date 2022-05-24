"""Novus Modbus Hub"""
from datetime import timedelta
import logging
import threading
from urllib.parse import urlparse

from homeassistant.core import CALLBACK_TYPE, callback
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client.sync import ModbusSerialClient, ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.register_read_message import ReadHoldingRegistersResponse
from voluptuous.validators import Number

from .const import FAULT_MESSAGES

_LOGGER = logging.getLogger(__name__)


class NovusModbusHub(DataUpdateCoordinator[dict]):
    """Class to manage fetching data from a Novus Controller."""

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

        parsed = urlparse(f'//{hostname}')

        # If it's not a URL it may be a serial port.
        if (parsed.port is None) and ((parsed.hostname is None) or
           (parsed.hostname[0:3] == "com")):
            self._client = ModbusSerialClient(
                    method='rtu',
                    port=parsed.path + parsed.netloc,
                    baudrate=9600,
                    stopbits=1,
                    bytesize=8,
                    timeout=5)
        else:
            if (parsed.port is None):
                localport = 502
            else:
                localport = parsed.port

            self._client = ModbusTcpClient(
                    host=parsed.hostname,
                    port=localport,
                    timeout=5)

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

    def _read(
        self, unit = 1, address = 0
    ) -> ReadHoldingRegistersResponse:
        """Read modbus holding registers."""
        with self._lock:
            kwargs = {"unit": unit} if unit else {}
            return self._client.read_holding_registers(
                    address, 4, **kwargs)

    async def _async_update_data(self) -> dict:
        realtime_data = {}
        try:
            realtime_data = await self.hass.async_add_executor_job(
                self.fetch
            )
        except ConnectionException:
            _LOGGER.error("novus modbus read failed.")
            realtime_data["faultmsg"] = "novus controller unreachable."

        return {**realtime_data}

    def fetch(self) -> dict:
        """Fetch data from novus controller"""
        data = {}

        # TODO: data can only be read 4 registers at a time,
        # abstract this out so we don't need to keep calling _read()
        resp = self._read()
        if resp.isError():
            return {}

        decoder = BinaryPayloadDecoder.fromRegisters(
            resp.registers,
            byteorder=Endian.Big,
            wordorder=Endian.Little
        )

        data["t1_temp_c"] = decoder.decode_16bit_int()
        data["t2_temp_c"] = decoder.decode_16bit_int()
        data["temp_diff_c"] = decoder.decode_16bit_int()
        # data["diff_setpoint_c_on"] = decoder.decode_16bit_int()

        # resp = self._read(address=4)
        # if resp.isError():
        #     return {}

        # data["diff_setpoint_c_off"] = decoder.decode_16bit_int()

        return data
