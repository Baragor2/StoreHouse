from uuid import UUID

from fastapi import APIRouter, status

from app.database import async_session_maker
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.dao import OrdersDAO
from app.orders.schemas import SOrder, Status

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_items: list[SOrderItemWithoutOrderId]) -> dict[str, str]:
    async with async_session_maker() as session:
        await OrdersDAO.create_order(session, order_items)
        await session.commit()
    return {"message": "Order created successfully"}


@router.get("/")
async def get_orders() -> list[SOrder]:
    async with async_session_maker() as session:
        orders: list[SOrder] = await OrdersDAO.find_all(session)
        await session.commit()
    return orders


@router.get("/{order_id}")
async def get_order(order_id: UUID) -> SOrder:
    async with async_session_maker() as session:
        order: SOrder = await OrdersDAO.get_order(session, order_id)
        await session.commit()
    return order


@router.patch("/{order_id}/status")
async def update_order_status(order_id: UUID, new_status: Status) -> dict[str, str]:
    async with async_session_maker() as session:
        await OrdersDAO.update_order_status(session, order_id, new_status)
        await session.commit()
    return {"message": "Order status updated successfully"}
