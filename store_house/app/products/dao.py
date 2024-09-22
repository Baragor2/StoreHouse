from uuid import UUID

from pydantic import PositiveInt
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import NoSuchProductException, NotEnoughProductsException
from app.products.models import Products
from app.products.schemas import SProductWithoutId, SProduct


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_product(cls, session: AsyncSession, product_id: UUID) -> SProduct:
        product = await ProductsDAO.find_one_or_none(session, id=product_id)
        if not product:
            raise NoSuchProductException
        return product

    @classmethod
    async def update_product(cls, session: AsyncSession, product_id: UUID, product: SProductWithoutId) -> None:
        await cls.get_product(session, product_id)

        update_product_stmt = (
            update(Products)
            .where(Products.id == product_id)
            .values(**dict(product))
        )

        await session.execute(update_product_stmt)

    @classmethod
    async def delete_product(cls, session: AsyncSession, product_id: UUID) -> None:
        await cls.get_product(session, product_id)

        delete_product_stmt = (
            delete(Products)
            .where(Products.id == product_id)
        )

        await session.execute(delete_product_stmt)

    @classmethod
    async def check_enough_products(
            cls,
            session: AsyncSession,
            product_id: UUID,
            product_count: PositiveInt
    ) -> None:
        product = await cls.get_product(session, product_id)
        if product.available < product_count:
            NotEnoughProductsException.detail = f'Недостаточно "{product.title}" на складе'
            raise NotEnoughProductsException

    @classmethod
    async def change_available_quantity(
            cls,
            session: AsyncSession,
            product_id: UUID,
            product_count: PositiveInt
    ) -> None:
        product = await cls.get_product(session, product_id)

        update_product_available_stmt = (
            update(Products)
            .where(Products.id == product_id)
            .values(available=product.available - product_count if product.available - product_count >= 0 else 0)
        )

        await session.execute(update_product_available_stmt)
