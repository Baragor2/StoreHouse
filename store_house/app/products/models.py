from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Products(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    available: Mapped[int] = mapped_column(nullable=False)
