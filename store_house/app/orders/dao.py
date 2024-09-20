from datetime import datetime, UTC
from uuid import uuid4

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.order_items.dao import OrderItemsDAO
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.models import Orders


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
