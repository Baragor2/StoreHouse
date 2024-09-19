from uuid import UUID

from fastapi import APIRouter

from app.products.dao import ProductsDAO
from app.products.schemas import SProduct

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/")
async def get_products() -> list[SProduct]:
    products = await ProductsDAO.find_all()
    return products


@router.get("/{product_id}")
async def get_product(product_id: UUID) -> SProduct:
    product = await ProductsDAO.find_one_or_none(id=product_id)
    return product
