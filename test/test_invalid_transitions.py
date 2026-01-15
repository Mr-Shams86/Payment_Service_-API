import pytest

from test.utils import create_payment


@pytest.mark.asyncio
async def test_cannot_refund_pending_payment(client):
    # pending -> refund
    r, payment, _ = await create_payment(client, order_id=40001, amount=10.0)
    pid = payment["id"]

    resp = await client.post(f"/api/v1/payments/{pid}/refund")
    assert resp.status_code in (400, 409)


@pytest.mark.asyncio
async def test_cannot_confirm_failed_payment(client):
    # pending -> failed
    r, payment, _ = await create_payment(client, order_id=40002, amount=10.0)
    pid = payment["id"]

    await client.post(f"/api/v1/payments/{pid}/fail")

    # failed -> confirm
    resp = await client.post(f"/api/v1/payments/{pid}/confirm")
    assert resp.status_code in (400, 409)


@pytest.mark.asyncio
async def test_cannot_fail_refunded_payment(client):
    # pending -> confirmed
    r, payment, _ = await create_payment(client, order_id=40003, amount=10.0)
    pid = payment["id"]

    await client.post(f"/api/v1/payments/{pid}/confirm")
    await client.post(f"/api/v1/payments/{pid}/refund")

    # refunded -> fail
    resp = await client.post(f"/api/v1/payments/{pid}/fail")
    assert resp.status_code in (400, 409)


@pytest.mark.asyncio
async def test_cannot_refund_twice(client):
    # pending -> confirmed -> refunded
    r, payment, _ = await create_payment(client, order_id=40004, amount=10.0)
    pid = payment["id"]

    await client.post(f"/api/v1/payments/{pid}/confirm")
    await client.post(f"/api/v1/payments/{pid}/refund")

    # refunded -> refunded
    resp = await client.post(f"/api/v1/payments/{pid}/refund")
    assert resp.status_code in (400, 409)


@pytest.mark.asyncio
async def test_confirm_indopotent_after_confirmed(client):
    # confirm уже confirmed - допустимо (индепотентность confirm)
    r, payment, _ = await create_payment(client, order_id=40005, amount=10.0)
    pid = payment["id"]

    r1 = await client.post(f"/api/v1/payments/{pid}/confirm")
    r2 = await client.post(f"/api/v1/payments/{pid}/confirm")

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_operations_on_nonexistent_payment(client):
    fake_id = 99999999

    r1 = await client.post(f"/api/v1/payments/{fake_id}/confirm")
    r2 = await client.post(f"/api/v1/payments/{fake_id}/fail")
    r3 = await client.post(f"/api/v1/payments/{fake_id}/refund")

    assert r1.status_code == 404
    assert r2.status_code == 404
    assert r3.status_code == 404
