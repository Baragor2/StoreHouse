from uuid import UUID, uuid4

from fastapi import APIRouter, status

from app.database import async_session_maker
from app.products.dao import ProductsDAO
from app.products.schemas import SProduct, SProductWithoutId

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/")
async def get_products() -> list[SProduct]:
    async with async_session_maker() as session:
        products = await ProductsDAO.find_all(session)
        session.commit()
    return products


@router.get("/{product_id}")
async def get_product(product_id: UUID) -> SProduct:
    async with async_session_maker() as session:
        product = await ProductsDAO.find_one_or_none(session, id=product_id)
        session.commit()
    return product


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        product: SProductWithoutId,
) -> dict[str, str]:
    async with async_session_maker() as session:
        await ProductsDAO.add(
            session,
            id=uuid4(),
            **dict(product)
        )
        session.commit()
    return {"message": "Product created"}


@router.put("/{product_id}")
async def update_product(
        product_id: UUID,
        product: SProductWithoutId,
) -> dict[str, str]:
    async with async_session_maker() as session:
        await ProductsDAO.update_product(session, product_id, product)
        session.commit()
    return {"message": "Product updated"}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: UUID,
) -> None:
    async with async_session_maker() as session:
        await ProductsDAO.delete_product(session, product_id)
        session.commit()
