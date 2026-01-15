from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate


class IdempotencyConflictError(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    """Когда пытаются сделать запрещённый переход статуса."""
    pass


ALLOWED_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    PaymentStatus.PENDING: {PaymentStatus.CONFIRMED, PaymentStatus.FAILED},
    PaymentStatus.CONFIRMED: {PaymentStatus.CONFIRMED, PaymentStatus.REFUNDED},
    PaymentStatus.FAILED: set(),
    PaymentStatus.REFUNDED: set(),
}


async def create_payment(
    data: PaymentCreate,
    idempotency_key: str,
    db: AsyncSession,
) -> tuple[Payment, bool]:

    result = await db.execute(
        select(Payment).where(Payment.idempotency_key == idempotency_key)
    )
    existing = result.scalar_one_or_none()

    if existing:
        if (
            existing.order_id != data.order_id
            or existing.amount != data.amount
            or existing.currency != data.currency
        ):
            raise IdempotencyConflictError(
                "Idempotency key reuse with different payload"
            )
        return existing, False

    payment = Payment(
        order_id=data.order_id,
        amount=data.amount,
        currency=data.currency,
        idempotency_key=idempotency_key,
    )
    db.add(payment)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()

        result = await db.execute(
            select(Payment).where(Payment.idempotency_key == idempotency_key)
        )
        existing = result.scalar_one()

        if (
            existing.order_id != data.order_id
            or existing.amount != data.amount
            or existing.currency != data.currency
        ):

            raise IdempotencyConflictError(
                "Idempotency key reuse with different payload"
            )
        return existing, False

    await db.refresh(payment)
    return payment, True


async def get_payment(payment_id: int, db: AsyncSession) -> Payment | None:
    result = await db.execute(
        select(Payment).where(Payment.id == payment_id))
    return result.scalar_one_or_none()


async def change_status(
    payment_id: int,
    new_status: PaymentStatus,
    db: AsyncSession,
) -> Payment | None:
    result = await db.execute(
        select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()

    if not payment:
        return None

    old_status = payment.status
    if isinstance(old_status, str):
        old_status = PaymentStatus(old_status)

    if isinstance(new_status, str):
        new_status = PaymentStatus(new_status)

    allowed = ALLOWED_TRANSITIONS.get(old_status, set())

    if new_status not in allowed:
        raise InvalidStatusTransitionError(
            f"{old_status} -> {new_status} is not allowed")

    payment.status = new_status
    await db.commit()
    await db.refresh(payment)
    return payment
