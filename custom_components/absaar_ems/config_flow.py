"""Config flow for Absaar Inverter integration."""
import logging
import voluptuous as vol
import requests
import urllib3

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, BASE_URL

urllib3.disable_warnings()

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_credentials(hass: HomeAssistant, username: str, password: str) -> dict:
    """Validate the user credentials by attempting to login."""
    url = f"{BASE_URL}/dn/userLogin"
    headers = {
        "User-Agent": "okhttp-okgo/jeasonlzy",
        "Content-Type": "application/json;charset=utf-8",
    }
    payload = {"username": username, "password": password}

    try:
        response = await hass.async_add_executor_job(
            lambda: requests.post(url, headers=headers, json=payload, verify=False, timeout=10)
        )
        data = response.json()

        if response.status_code == 200 and "token" in data:
            return {"token": data["token"], "user_id": data["userId"]}
        else:
            _LOGGER.error("Login failed: %s", data)
            return None
    except requests.exceptions.RequestException as e:
        _LOGGER.error("Error during login: %s", e)
        return None


class AbsaarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Absaar Inverter."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate credentials
            result = await validate_credentials(
                self.hass,
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD]
            )

            if result:
                # Create a unique ID based on the username
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Absaar ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
