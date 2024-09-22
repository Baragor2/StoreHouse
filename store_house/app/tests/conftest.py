import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app

from app.order_items.models import OrderItems
from app.orders.models import Orders
from app.products.models import Products


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.mode.mode == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    products = open_mock_json("products")
    orders = open_mock_json("orders")
    order_items = open_mock_json("order_items")

    for order in orders:
        order["creation_date"] = datetime.strptime(order["creation_date"], "%Y-%m-%d %H:%M:%S")

    async with async_session_maker() as session:
        for Model, values in [
            (Products, products),
            (Orders, orders),
            (OrderItems, order_items),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
