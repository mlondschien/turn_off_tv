"""Platform for light integration."""
from __future__ import annotations
import wakeonlan
import logging
import voluptuous as vol
# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_PORT, CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from samsungtvws import SamsungTVWS
from typing import Any

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.REQUIRED(CONF_HOST): cv.string,
    vol.REQUIRED(CONF_MAC): cv.string,
    vol.OPTIONAL(CONF_PORT, default=8002): cv.port,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up Samsung TV connection."""
    ip = config.get(CONF_HOST)

    tv = SamsungTVWS(ip)
    # Assign configuration variables.
    # The configuration check takes care they are present.

    host = config[CONF_HOST]
    mac_address = config[CONF_MAC]
    port = config.get(CONF_PORT)

    # Add devices
    add_entities(SamsungFrame(host=host, port=port, mac_adress=mac_address))


class SamsungFrame(LightEntity, SamsungTVWS):
    """Representation of Samsung Frame TV."""

    def __init__(self, host, port, mac_adress=None) -> None:
        """Initialize an AwesomeLight."""
        self.mac_adress = mac_adress.replace(":", ".")
        super(self, SamsungTVWS).__init__(host, port=port)
    
    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self.is_alive()
    
    def turn_on(self, **kwargs: Any) -> None:
        wakeonlan.send_magic_packet(self.mac_adress)
    
    def turn_off(self, **kwargs: Any) -> None:
        self.hold_key("KEY_POWER", seconds=3)
