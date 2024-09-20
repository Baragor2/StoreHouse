from datetime import datetime, UTC
from uuid import uuid4

from fastapi import APIRouter, status

from app.order_items.dao import OrderItemsDAO
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.dao import OrdersDAO

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_items: list[SOrderItemWithoutOrderId]) -> dict[str, str]:
    order_id = uuid4()

    await OrderItemsDAO.create_order_items_from_list(order_id, order_items)
    await OrdersDAO.add(
        id=order_id,
        creation_date=datetime.now(UTC),
        status="В процессе",
    )
    return {"message": "Order created successfully"}
