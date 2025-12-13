from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate


async def create_payment(data: PaymentCreate, db: AsyncSession) -> Payment:
    payment = Payment(
        order_id=data.order_id,
        amount=data.amount,
        currency=data.currency,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def get_payment(payment_id: int, db: AsyncSession) -> Payment | None:
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def change_status(
    payment_id: int,
    new_status: PaymentStatus,
    db: AsyncSession,
) -> Payment | None:
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()

    if not payment:
        return None

    payment.status = new_status
    await db.commit()
    await db.refresh(payment)
    return payment
