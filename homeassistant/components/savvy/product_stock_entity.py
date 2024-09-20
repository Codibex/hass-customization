"""Module for representing a Product Stock entity in Home Assistant."""

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


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

        self.entity_id = f"sensor.savvy_{self._name.lower()}"

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
        }
