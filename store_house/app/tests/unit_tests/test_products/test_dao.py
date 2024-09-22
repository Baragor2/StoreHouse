from uuid import UUID

import pytest
from pydantic import PositiveInt

from app.exceptions import NoSuchProductException, NotEnoughProductsException
from app.products.dao import ProductsDAO


@pytest.mark.parametrize("product_id,product_title,is_product_present", [
    ("bde7bbfc-5a12-4e3c-ab7d-ea02bdc46560", "Стул", True),
    ("c566bb72-9d21-4702-a3cc-3eec6c86f200", "Кресло", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf8ac01fa", "Несуществующий товар", False),
])
async def test_find_product_by_id(
        product_id: UUID,
        product_title: str,
        is_product_present: bool,
) -> None:
    product = await ProductsDAO.find_one_or_none(id=product_id)

    if is_product_present:
        assert product
        assert product.title == product_title
    else:
        assert not product


@pytest.mark.parametrize("product_id,is_product_present", [
    ("e00c1ca7-ce4a-4bc2-a4cb-b2e2003abb05", True),
    ("e7669593-2ca0-407e-b0c2-cd9bf5397047", True),
    ("6e67bd30-3d3a-42dd-a764-71a2d91649e6", True),
    ("6e67bd30-3d3a-42dd-a764-71a2d91649e8", False),
])
async def test_delete_product(product_id: UUID, is_product_present: bool) -> None:
    try:
        await ProductsDAO.delete_product(product_id)

        product = await ProductsDAO.find_one_or_none(id=product_id)
        assert not product
    except NoSuchProductException:
        assert not is_product_present


@pytest.mark.parametrize("product_id,product_count,is_enough_products", [
    ("8860bb15-cd0e-4dcf-b5ee-926e1d5395f2", 3, False),
    ("9d5185a0-4ebd-4a42-8852-c44671bf3368", 4, True),
    ("e5a52008-66fa-4212-921e-727c4aac680d", 5, True),
])
async def test_check_enough_products(
        product_id: UUID,
        product_count: PositiveInt,
        is_enough_products: bool,
) -> None:
    try:
        await ProductsDAO.check_enough_products(product_id, product_count)
        assert is_enough_products
    except NotEnoughProductsException:
        assert not is_enough_products


@pytest.mark.parametrize("product_id,product_count,expected_product_count", [
    ("bde7bbfc-5a12-4e3c-ab7d-ea02bdc46560", 15, 0),
    ("25d69dda-fb13-44b5-8f4b-c41a7292cb39", 5, 0),
    ("c566bb72-9d21-4702-a3cc-3eec6c86f200", 3, 5),
])
async def test_change_available_quantity(
        product_id: UUID,
        product_count: PositiveInt,
        expected_product_count: PositiveInt,
) -> None:
    await ProductsDAO.change_available_quantity(product_id, product_count)
    product = await ProductsDAO.get_product(product_id)
    assert product.available == expected_product_count
