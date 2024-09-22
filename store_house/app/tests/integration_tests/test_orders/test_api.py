import pytest
from httpx import AsyncClient
from pydantic import PositiveInt

from app.database import async_session_maker
from app.order_items.dao import OrderItemsDAO
from app.orders.dao import OrdersDAO
from app.products.dao import ProductsDAO
from app.products.schemas import SProduct


@pytest.mark.parametrize(
    "order_items_list,expected_products_count,expected_orders_count,expected_order_items_count,status_code", [
    (
        [
            {
                "product_id": "8860bb15-cd0e-4dcf-b5ee-926e1d5395f2",
                "quantity_in_order": 1
            },
            {
                "product_id": "9d5185a0-4ebd-4a42-8852-c44671bf3368",
                "quantity_in_order": 3
            },
        ],
        [1, 1],
        4,
        6,
        201,
    ),
    (
        [
            {
                "product_id": "e5a52008-66fa-4212-921e-727c4aac680d",
                "quantity_in_order": 20
            },
            {
                "product_id": "e00c1ca7-ce4a-4bc2-a4cb-b2e2003abb05",
                "quantity_in_order": 10
            },
        ],
        [15, 3],
        3,
        4,
        400,
    ),
])
async def test_create_order(
    order_items_list: list[dict],
    expected_products_count: list[PositiveInt],
    expected_orders_count: PositiveInt,
    expected_order_items_count: PositiveInt,
    status_code: PositiveInt,
    ac: AsyncClient,
) -> None:
    response = await ac.post(
        f"/orders/",
        json=order_items_list
    )
    async with async_session_maker() as session:
        orders_count = len(await OrdersDAO.find_all(session))
        assert orders_count == expected_orders_count

        order_items_count = len(await OrderItemsDAO.find_all(session))
        assert order_items_count == expected_order_items_count

        for ind, order_item in enumerate(order_items_list):
            product: SProduct = await ProductsDAO.find_one_or_none(session, id=order_item.get("product_id"))
            assert product.available == expected_products_count[ind]

        assert response.status_code == status_code
        await session.commit()
