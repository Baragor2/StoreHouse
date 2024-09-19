from uuid import UUID

from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import NoSuchProductException
from app.products.models import Products
from app.products.schemas import SProductWithoutId, SProduct


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_product(cls, product_id: UUID) -> SProduct:
        product = await ProductsDAO.find_one_or_none(id=product_id)
        if not product:
            raise NoSuchProductException
        return product

    @classmethod
    async def update_product(cls, product_id: UUID, product: SProductWithoutId) -> None:
        await cls.get_product(product_id)

        async with async_session_maker() as session:
            update_product_stmt = (
                update(Products)
                .where(Products.id == product_id)
                .values(**dict(product))
            )

        await session.execute(update_product_stmt)
        await session.commit()

    @classmethod
    async def delete_product(cls, product_id: UUID) -> None:
        await cls.get_product(product_id)

        async with async_session_maker() as session:
            delete_product_stmt = (
                delete(Products)
                .where(Products.id == product_id)
            )

            await session.execute(delete_product_stmt)
            await session.commit()
