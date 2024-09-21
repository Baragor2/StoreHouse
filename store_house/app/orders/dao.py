from datetime import datetime, UTC
from uuid import uuid4, UUID

from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NoSuchOrderException
from app.order_items.dao import OrderItemsDAO
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.models import Orders
from app.orders.schemas import SOrder, Status


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def create_order(cls, order_items: list[SOrderItemWithoutOrderId]) -> None:
        order_id = uuid4()

        async with async_session_maker() as session:
            await OrdersDAO.add(
                id=order_id,
                creation_date=datetime.now(UTC).replace(tzinfo=None),
                status="В процессе",
            )
            await OrderItemsDAO.create_order_items_from_list(order_id, order_items)
            await session.commit()

    @classmethod
    async def get_order(cls, order_id: UUID) -> SOrder:
        order: SOrder = await OrdersDAO.find_one_or_none(id=order_id)
        if not order:
            raise NoSuchOrderException
        return order

    @classmethod
    async def update_order_status(cls, order_id: UUID, new_status: Status) -> None:
        await OrdersDAO.get_order(order_id)

        async with async_session_maker() as session:
            update_product__available_stmt = (
                update(Orders)
                .where(Orders.id == order_id)
                .values(status=new_status)
            )

        await session.execute(update_product__available_stmt)
        await session.commit()
