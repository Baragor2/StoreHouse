from uuid import UUID

import pytest

from app.database import async_session_maker
from app.exceptions import NoSuchOrderException
from app.orders.dao import OrdersDAO
from app.orders.schemas import Status


@pytest.mark.parametrize("order_id,is_order_present", [
    ("0389467f-3d5c-4c0c-8e57-ed53ffa69872", True),
    ("5a9d8411-e4a9-45ce-9530-dcb6b80ef504", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf8ac01fa", False),
])
async def test_find_order_by_id(
        order_id: UUID,
        is_order_present: bool,
) -> None:
    async with async_session_maker() as session:
        order = await OrdersDAO.find_one_or_none(session, id=order_id)
        await session.commit()
    if is_order_present:
        assert order
    else:
        assert not order


@pytest.mark.parametrize("order_id,new_status,is_order_present", [
    ("0389467f-3d5c-4c0c-8e57-ed53ffa69872", "В процессе", True),
    ("5a9d8411-e4a9-45ce-9530-dcb6b80ef504", "Доставлен", True),
    ("b1f574aa-14a1-4254-aa81-76dbb47ddc9d", "В процессе", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf8ac01fa", "...", False),
])
async def test_update_order_status(
        order_id: UUID,
        new_status: Status,
        is_order_present: bool,
) -> None:
    try:
        async with async_session_maker() as session:
            await OrdersDAO.update_order_status(session, order_id, new_status)
            product = await OrdersDAO.get_order(session, order_id)
            assert product.status == new_status
            await session.commit()
    except NoSuchOrderException:
        assert not is_order_present
