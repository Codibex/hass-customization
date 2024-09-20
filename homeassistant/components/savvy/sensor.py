"""Module sets up Savvy sensor entities from a config entry."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .product_stock_entity import ProductStockEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Savvy sensor entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    product_stocks = coordinator.data

    entities = [
        ProductStockEntity(coordinator, stock) for stock in product_stocks.values()
    ]

    for entity in entities:
        coordinator.entities[entity.entity_id] = entity

    async_add_entities(entities)
