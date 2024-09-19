from decimal import Decimal
from typing import Annotated
from uuid import UUID

from annotated_types import Gt
from pydantic import BaseModel, PositiveInt


class SProduct(BaseModel):
    id: UUID
    title: str
    description: str
    price: Annotated[Decimal, Gt(0)]
    available: PositiveInt
