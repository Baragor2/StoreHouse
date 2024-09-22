from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.order_items.models import OrderItems
from app.order_items.schemas import SOrderItemWithoutOrderId
from app.products.dao import ProductsDAO


class OrderItemsDAO(BaseDAO):
    model = OrderItems

    @classmethod
    async def create_order_items_from_list(
            cls,
            session: AsyncSession,
            order_id: UUID,
            order_items: list[SOrderItemWithoutOrderId],
    ) -> None:
        for order_item in order_items:
            await cls.create_order_item(session, order_id, order_item)

    @classmethod
    async def create_order_item(
            cls,
            session: AsyncSession,
            order_id: UUID,
            order_item: SOrderItemWithoutOrderId,
    ) -> None:
        await ProductsDAO.check_enough_products(
            session,
            order_item.product_id,
            order_item.quantity_in_order,
        )
        await ProductsDAO.change_available_quantity(
            session,
            order_item.product_id,
            order_item.quantity_in_order,
        )

        await cls.add(
            session,
            order_id=order_id,
            **dict(order_item),
        )
