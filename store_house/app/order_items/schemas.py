from uuid import UUID

from pydantic import BaseModel, PositiveInt


class SOrderItem(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity_in_order: PositiveInt
