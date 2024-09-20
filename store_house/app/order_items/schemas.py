from uuid import UUID

from pydantic import BaseModel, PositiveInt


class SOrderItem(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity_in_order: PositiveInt


class SOrderItemWithoutOrderId(BaseModel):
    product_id: UUID
    quantity_in_order: PositiveInt
