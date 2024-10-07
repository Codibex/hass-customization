"""Module for representing a Product Stock entity in Home Assistant."""

import re
import unicodedata

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


def normalize_entity_id(name):
    """Normalize the entity ID by removing invalid characters and replacing diacritics."""
    # Replace German umlauts and other common diacritics
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",  # pylint: disable=invalid-name
        "ß": "ss",
        "é": "e",
        "è": "e",
        "ê": "e",
        "à": "a",
        "á": "a",
        "â": "a",
        "ç": "c",
        # Add more replacements as needed
    }
    for original, replacement in replacements.items():
        name = name.replace(original, replacement)

    # Normalize the name to NFKD form
    normalized_name = unicodedata.normalize("NFKD", name)
    # Encode to ASCII bytes, ignore errors, and decode back to string
    ascii_name = normalized_name.encode("ascii", "ignore").decode("ascii")
    # Replace any remaining invalid characters with underscores
    entity_id = re.sub(r"[^a-zA-Z0-9_]", "_", ascii_name)
    return entity_id.lower()


class ProductStockEntity(CoordinatorEntity):
    """Representation of a Product Stock."""

    def __init__(
        self,
        coordinator,
        stock,
    ) -> None:
        """Initialize the entity."""

        super().__init__(coordinator)
        self._product_id = stock["productId"]
        self._name = stock["name"]
        self._quantity = stock["quantity"]
        self._min_quantity = stock["minQuantity"]
        self._max_quantity = stock["maxQuantity"]
        self._notification_quantity = stock["notificationQuantity"]
        self._should_notify_on_quantity = stock["shouldNotifyOnQuantity"]

        self.entity_id = f"sensor.savvy_{normalize_entity_id(self._name)}"
        self._attr_unique_id = (
            f"savvy_{self._product_id}_{normalize_entity_id(self._name)}"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        stock = self.coordinator.data.get(self._product_id)
        if stock:
            self._quantity = stock["quantity"]
            self._min_quantity = stock["minQuantity"]
            self._max_quantity = stock["maxQuantity"]
            self._notification_quantity = stock["notificationQuantity"]
            self.async_write_ha_state()

    async def async_update_stock(self, adjustmentType, amount):
        """Call the coordinator to update stock."""
        await self.coordinator.async_update_stock(
            self._product_id, adjustmentType, amount
        )

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def state(self):
        """Return the state of the entity."""
        return self._quantity

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "min_quantity": self._min_quantity,
            "max_quantity": self._max_quantity,
            "notification_quantity": self._notification_quantity,
            "should_notify_on_quantity": self._should_notify_on_quantity,
        }
