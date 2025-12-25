import pytest

from utils import create_payment


@pytest.mark.asyncio
async def test_create_payment_returns_201(client):
    r, _ = await create_payment(client, order_id=10001, amount=10.0)
    assert r.status_code == 201

    body = r.json()
    assert body["id"] > 0
    assert body["order_id"] == 10001
    assert body["amount"] == 10.0
    assert body["currency"] == "USD"
    assert body["status"] == "pending"
    assert "created_at" in body
    assert "updated_at" in body


@pytest.mark.asyncio
async def test_get_payment_by_id(client):
    r, _ = await create_payment(client, order_id=10002, amount=20.0)
    pid = r.json()["id"]

    r2 = await client.get(f"/api/v1/payments/{pid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == pid


@pytest.mark.asyncio
async def test_get_payment_not_found(client):
    r = await client.get("/api/v1/payments/99999999999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_payment_validation_error(client):
    # amount отрецательный -> ожидаем 422 от pydantic/fastapi
    r = await client.post(
        "/api/v1/payments/",
        headers={"Indepotency-Key": "bad-key"},
        json={
            "order_id": 1,
            "amount": -1,
            "currency": "USD"},  # amount < 0
    )
    assert r.status_code == 422
