from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class OrderItems(Base):
    __tablename__ = 'order_items'

    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), primary_key=True, nullable=False)
    quantity_in_order: Mapped[int] = mapped_column(nullable=False)
