from fastapi import APIRouter, status

from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.dao import OrdersDAO

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_items: list[SOrderItemWithoutOrderId]) -> dict[str, str]:
    await OrdersDAO.create_order(order_items)
    return {"message": "Order created successfully"}


