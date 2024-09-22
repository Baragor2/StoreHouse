from datetime import datetime, UTC
from uuid import uuid4, UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import NoSuchOrderException
from app.order_items.dao import OrderItemsDAO
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.orders.models import Orders
from app.orders.schemas import SOrder, Status


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def create_order(
            cls,
            session: AsyncSession,
            order_items: list[SOrderItemWithoutOrderId]
    ) -> None:
        order_id = uuid4()

        await OrdersDAO.add(
            session,
            id=order_id,
            creation_date=datetime.now(UTC).replace(tzinfo=None),
            status="В процессе",
        )
        await OrderItemsDAO.create_order_items_from_list(session, order_id, order_items)
        await session.commit()

    @classmethod
    async def get_order(cls, session: AsyncSession, order_id: UUID) -> SOrder:
        order: SOrder = await OrdersDAO.find_one_or_none(session, id=order_id)
        if not order:
            raise NoSuchOrderException
        return order

    @classmethod
    async def update_order_status(
            cls,
            session: AsyncSession,
            order_id: UUID,
            new_status: Status
    ) -> None:
        await OrdersDAO.get_order(session, order_id)

        update_product_available_stmt = (
            update(Orders)
            .where(Orders.id == order_id)
            .values(status=new_status)
        )

        await session.execute(update_product_available_stmt)
