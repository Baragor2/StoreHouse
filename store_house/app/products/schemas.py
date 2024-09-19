from decimal import Decimal
from typing import Annotated, TypeAlias
from uuid import UUID

from annotated_types import Ge
from pydantic import BaseModel, PositiveInt

Price: TypeAlias = Annotated[Decimal, Ge(0)]


class SProduct(BaseModel):
    id: UUID
    title: str
    description: str
    price: Price
    available: PositiveInt


class SProductWithoutId(BaseModel):
    title: str
    description: str
    price: Price
    available: PositiveInt
