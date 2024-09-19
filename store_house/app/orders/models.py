from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
