from uuid import UUID

from fastapi import APIRouter, status

from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.dao import OrdersDAO
from app.orders.schemas import SOrder, Status

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_items: list[SOrderItemWithoutOrderId]) -> dict[str, str]:
    await OrdersDAO.create_order(order_items)
    return {"message": "Order created successfully"}


@router.get("/")
async def get_orders() -> list[SOrder]:
    orders: list[SOrder] = await OrdersDAO.find_all()
    return orders


@router.get("/{order_id}")
async def get_order(order_id: UUID) -> SOrder:
    order: SOrder = await OrdersDAO.get_order(order_id)
    return order


@router.patch("/{order_id}/status")
async def update_order_status(order_id: UUID, new_status: Status) -> dict[str, str]:
    await OrdersDAO.update_order_status(order_id, new_status)
    return {"message": "Order status updated successfully"}
