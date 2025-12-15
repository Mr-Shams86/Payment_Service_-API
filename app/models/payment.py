import enum
from datetime import datetime

from sqlalchemy import String, Enum, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True
    )

    provider: Mapped[str] = mapped_column(String(32), default="fake")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    idempotency_key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
