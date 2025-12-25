import pytest

from utils import create_payment, new_key


@pytest.mark.asyncio
async def test_idempotency_same_key_same_payload_returns_same_payment(client):
    key = new_key("idem")
    r1, _ = await create_payment(
        client,
        order_id=20001,
        amount=10.0, key=key)

    assert r1.status_code == 201
    id1 = r1.json()["id"]

    # повторяем тот же запрос с тем же ключом и тем же payload
    r2 = await client.post(
        "/api/v1/payments/",
        headers={"Idempotency-Key": key},
        json={
            "order_id": 20001,
            "amount": 10.0,
            "currency": "USD"},
    )

    assert r2.status_code in (200, 201)
    assert r2.json()["id"] == id1


@pytest.mark.asyncio
async def test_idempotency_same_key_different_payload_returns_409(client):
    key = new_key("idem")
    r1, _ = await create_payment(
        client,
        order_id=20002,
        amount=10.0,
        key=key)

    assert r1.status_code == 201

    id1 = r1.json()["id"]
    assert isinstance(id1, int) and id1 > 0

    # тот же ключ, но payload другой
    r2 = await client.post(
        "/api/v1/payments/",
        headers={"Idempotency-Key": key},
        json={
            "order_id": 20002,
            "amount": 99.0,
            "currency": "USD"},
    )

    assert r2.status_code == 409
