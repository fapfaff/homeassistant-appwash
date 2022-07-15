"""Config flow for AppWash integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from appwashpy import check_credentials
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_LOCATION, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_LOCATION): str,
    }
)


def validate_credentials(email, password) -> bool:
    """Checks if the email and password combination is valid."""
    try:
        return check_credentials(email, password)
    except Exception as exc:
        raise CannotConnect() from exc


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    email = data[CONF_EMAIL]
    password = data[CONF_PASSWORD]
    location = data[CONF_LOCATION]

    if not await hass.async_add_executor_job(validate_credentials, email, password):
        raise InvalidAuth

    # Return info that you want to store in the config entry.
    return {
        "title": "AppWash",
        CONF_EMAIL: email,
        CONF_PASSWORD: password,
        CONF_LOCATION: location,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AppWash."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
