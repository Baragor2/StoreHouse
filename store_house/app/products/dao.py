from uuid import UUID

from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.products.models import Products
from app.products.schemas import SProductWithoutId


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def update_product(cls, product_id: UUID, product: SProductWithoutId) -> None:
        await cls.find_one_or_none(id=product_id)

        async with async_session_maker() as session:
            update_product_stmt = (
                update(Products)
                .where(Products.id == product_id)
                .values(**dict(product))
            )

        await session.execute(update_product_stmt)
        await session.commit()
