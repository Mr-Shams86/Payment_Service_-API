import uuid


def new_key(prefix: str = "idem") -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_payment(
    client, *,
    order_id: int,
    amount: float,
    currency: str = "USD",
    key: str | None = None
):

    key = key or new_key()
    r = await client.post(
        "/api/v1/payments/",
        headers={
            "Idempotency-Key": key},
        json={
            "order_id": order_id,
            "amount": amount,
            "currency": currency},
    )
    payment = r.json() if r.headers.get("content-type", "").startswith(
        "application/json") else None
    return r, payment, key
