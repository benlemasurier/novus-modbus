import pytest
from homeassistant import config_entries, setup
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL

from custom_components.novus_modbus import DOMAIN
from custom_components.novus_modbus.const import (
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
)

@pytest.mark.asyncio
async def test_async_setup_component(hass):
    """Test the component gets set up and config_flow registered."""
    # Set up the custom component
    assert await setup.async_setup_component(hass, DOMAIN, {}) is True

    # Check if the config_flow has been registered
    flow = next(
        (
            flow
            for flow in hass.config_entries.flow.async_progress()
            if flow["handler"] == DOMAIN
        ),
        None,
    )

    # Test config_flow registration
    assert flow is not None
    assert flow["step_id"] == "user"
    assert flow["context"] == {"source": config_entries.SOURCE_USER}

    # Test config_flow data schema
    data_schema = flow["data_schema"]
    assert data_schema({CONF_NAME: DEFAULT_NAME}) == {CONF_NAME: DEFAULT_NAME}
    assert data_schema({CONF_HOST: "localhost"}) == {CONF_HOST: "localhost"}
    assert (
        data_schema({CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL})
        == {CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL}
    )
