
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Header,
    Response,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services.payments import (
    create_payment,
    get_payment,
    change_status,
    IdempotencyConflictError,
    InvalidStatusTransitionError,
)
from app.models.payment import PaymentStatus


router = APIRouter(prefix="/payments", tags=["payments"])


@router.post(
    "/", response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED
    )
async def create_payment_endpoint(
    payload: PaymentCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    try:
        payment, created = await create_payment(payload, idempotency_key, db)
    except IdempotencyConflictError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Idempotency key reused with different payload",
        )

    if not created:
        response.status_code = status.HTTP_200_OK

    return payment


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment_endpoint(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    payment = await get_payment(payment_id, db)
    if not payment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Payment not found")
    return payment


@router.post("/{payment_id}/confirm", response_model=PaymentRead)
async def confirm_payment_endpoint(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        payment = await change_status(payment_id, PaymentStatus.CONFIRMED, db)
    except InvalidStatusTransitionError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Invalid status transition")

    if not payment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Payment not found")

    return payment


@router.post("/{payment_id}/fail", response_model=PaymentRead)
async def fail_payment_endpoint(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        payment = await change_status(payment_id, PaymentStatus.FAILED, db)
    except InvalidStatusTransitionError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Invalid status transition")

    if not payment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Payment not found")

    return payment


@router.post("/{payment_id}/refund", response_model=PaymentRead)
async def refund_payment_endpoint(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        payment = await change_status(payment_id, PaymentStatus.REFUNDED, db)
    except InvalidStatusTransitionError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Invalid status transition")

    if not payment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Payment not found")

    return payment
