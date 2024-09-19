from datetime import datetime
from typing import TypeAlias, Literal
from uuid import UUID

from pydantic import BaseModel

Status: TypeAlias = Literal[
    "В процессе",
    "Отправлен",
    "Доставлен",
]


class SOrder(BaseModel):
    id: UUID
    creation_date: datetime
    status: Status
