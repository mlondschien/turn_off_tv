"""Test component setup."""
from homeassistant.setup import async_setup_component

from custom_components.turn_off_frame.const import DOMAIN


async def test_async_setup(hass):
    """Test the component gets setup."""
    assert await async_setup_component(hass, DOMAIN, {}) is True
