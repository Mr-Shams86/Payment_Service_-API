import pytest

from test.utils import create_payment


@pytest.mark.asyncio
async def test_confirm_payment(client):
    r, _, _ = await create_payment(client, order_id=30001, amount=10.0)
    pid = r.json()["id"]

    r2 = await client.post(f"/api/v1/payments/{pid}/confirm")
    assert r2.status_code == 200
    assert r2.json()["status"] == "confirmed"

    r3 = await client.get(f"/api/v1/payments/{pid}")
    assert r3.status_code == 200
    assert r3.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_fail_flow(client):
    r, _, _ = await create_payment(client, order_id=30002, amount=10.0)
    pid = r.json()["id"]

    r2 = await client.post(f"/api/v1/payments/{pid}/fail")
    assert r2.status_code == 200
    assert r2.json()["status"] == "failed"


@pytest.mark.asyncio
async def test_refund_flow(client):
    r, _, _ = await create_payment(client, order_id=30003, amount=10.0)
    pid = r.json()["id"]

    r_confirm = await client.post(f"/api/v1/payments/{pid}/confirm")
    assert r_confirm.status_code == 200
    assert r_confirm.json()["status"] == "confirmed"

    r2 = await client.post(f"/api/v1/payments/{pid}/refund")
    assert r2.status_code == 200
    assert r2.json()["status"] == "refunded"
