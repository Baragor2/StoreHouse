from uuid import UUID, uuid4

from fastapi import APIRouter, status

from app.products.dao import ProductsDAO
from app.products.schemas import SProduct, SProductWithoutId

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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        product: SProductWithoutId,
) -> dict[str, str]:
    await ProductsDAO.add(
        id=uuid4(),
        **dict(product)
    )
    return {"message": "Product created"}
