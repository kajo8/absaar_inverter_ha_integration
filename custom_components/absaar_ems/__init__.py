"""The Absaar Inverter integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .api import AbsaarAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(minutes=2)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Absaar Inverter from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    # Create API instance
    api = AbsaarAPI(username, password)

    # Authenticate
    if not await hass.async_add_executor_job(api.authenticate):
        _LOGGER.error("Failed to authenticate with Absaar API")
        return False

    # Create coordinator
    coordinator = AbsaarDataUpdateCoordinator(hass, api)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class AbsaarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Absaar data."""

    def __init__(self, hass: HomeAssistant, api: AbsaarAPI) -> None:
        """Initialize."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            return await self.hass.async_add_executor_job(self.api.fetch_all_data)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
