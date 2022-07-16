"""Support for AppWash Services as Sensor."""
from __future__ import annotations

import logging

from appwashpy import AppWash, Service
from appwashpy.common.enums import SERVICE_TYPE, STATE

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SERVICE_BUY_SERVICE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""

    appwash: AppWash = hass.data[DOMAIN][entry.entry_id]

    services = await hass.async_add_executor_job(appwash.services)

    entities = []
    for service in services:
        entities.append(AppWashStateSensor(appwash, service))
    async_add_entities(entities)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(SERVICE_BUY_SERVICE, {}, "buy_service")


class AppWashStateSensor(SensorEntity):
    """Representation AppWash Service State."""

    _attr_name = "AppWash Service"
    _attr_state_class: str
    _attr_native_value = "UNKNOWN"

    _appwash: AppWash
    _location_id: str

    def __init__(self, appwash: AppWash, service: Service) -> None:
        """Create a sensor for the state of an AppWash Service."""
        self._appwash = appwash
        self._location_id = service.location_id

        self._attr_unique_id = service.service_id
        self._attr_name = service.name + " " + service.service_id
        self._service_type = service.type

        self.set_icon()

    def set_icon(self):
        """Set the icon based on the service type and the current state."""
        state = ""
        if self._attr_native_value == STATE.AVAILABLE.name:
            state = ""
        elif self._attr_native_value == STATE.STOPPABLE.name:
            state = "-alert"
        elif self._attr_native_value == STATE.OCCUPIED.name:
            state = "-off"
        elif self._attr_native_value == STATE.FAULTED.name:
            state = "-off"

        if self._service_type == SERVICE_TYPE.WASHING_MACHINE.name:
            self._attr_icon = f"mdi:washing-machine{state}"
        elif self._service_type == SERVICE_TYPE.DRYER.name:
            self._attr_icon = f"mdi:tumble-dryer{state}"
        elif self._service_type == SERVICE_TYPE.ELECTRICITY.name:
            self._attr_icon = "mdi:lightning-bolt"

    def update(self) -> None:
        """Fetch new state data for the sensor."""

        service: Service = self._appwash.service(self.unique_id)
        self._attr_native_value = service.state
        self.set_icon()

    def buy_service(self) -> None:
        """Buy and start the AppWash service."""
        _LOGGER.info("Buying AppWash-Service %s", self.unique_id)
        self._appwash.buy_service(self.unique_id, safe=True)

    def stop_service(self) -> None:
        """Stop the AppWash service."""
        _LOGGER.info("Stopping AppWash-Service %s", self.unique_id)
        self._appwash.stop_service(self.unique_id)

    @property
    def device_info(self):
        """Information about the device the sensor belongs to."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self._attr_name,
            "areaId": self._location_id,
            "manufacturer": "Miele",
        }
