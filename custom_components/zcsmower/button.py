"""ZCS Lawn Mower Robot button platform."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.helpers.entity import (
    Entity,
    EntityCategory,
)

from .coordinator import ZcsMowerDataUpdateCoordinator
from .entity import ZcsMowerRobotEntity

ROBOT_ENTITY_DESCRIPTIONS = (
    ButtonEntityDescription(
        key="update_now",
        icon="mdi:update",
        translation_key="update_now",
        device_class=ButtonDeviceClass.UPDATE,
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="update_position",
        icon="mdi:update",
        translation_key="update_position",
        device_class=ButtonDeviceClass.UPDATE,
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="wake_up",
        icon="mdi:connection",
        translation_key="wake_up",
        device_class=ButtonDeviceClass.UPDATE,
    ),
    ButtonEntityDescription(
        key="work_now",
        icon="mdi:state-machine",
        translation_key="work_now",
        device_class=ButtonDeviceClass.UPDATE,
    ),
    ButtonEntityDescription(
        key="charge_now",
        icon="mdi:ev-station",
        translation_key="charge_now",
        device_class=ButtonDeviceClass.UPDATE,
    ),
    ButtonEntityDescription(
        key="border_cut",
        icon="mdi:scissors-cutting",
        translation_key="border_cut",
        device_class=ButtonDeviceClass.UPDATE,
    ),
    ButtonEntityDescription(
        key="trace_position",
        icon="mdi:map-marker",
        translation_key="trace_position",
        device_class=ButtonDeviceClass.UPDATE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: Entity,
) -> None:
    """Do setup buttons from a config entry created in the integrations UI."""
    coordinator = config_entry.runtime_data
    async_add_entities(
        [
            ZcsMowerRobotButtonEntity(
                hass=hass,
                config_entry=config_entry,
                coordinator=coordinator,
                entity_description=entity_description,
                imei=imei,
            )
            for imei in coordinator.mowers
            for entity_description in ROBOT_ENTITY_DESCRIPTIONS
        ],
        update_before_add=True,
    )


class ZcsMowerRobotButtonEntity(ZcsMowerRobotEntity, ButtonEntity):
    """Representation of a ZCS Lawn Mower Robot button."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        coordinator: ZcsMowerDataUpdateCoordinator,
        entity_description: ButtonEntityDescription,
        imei: str,
    ) -> None:
        """Initialize the button class."""
        super().__init__(
            hass=hass,
            config_entry=config_entry,
            coordinator=coordinator,
            entity_type="button",
            entity_description=entity_description,
            imei=imei,
        )

    async def async_press(self) -> None:
        """Press the button."""
        await getattr(self.coordinator, f"async_{self._entity_key}")(
            imei=self._imei,
        )
