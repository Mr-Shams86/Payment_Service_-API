# Payment Service API

A lightweight, production‑oriented **Payment Service** built with **FastAPI**, designed to handle payment lifecycle management in a microservices architecture.

This service demonstrates real‑world backend patterns: idempotent payment creation, explicit state transitions, RESTful endpoints, Dockerized infrastructure, and clear API documentation.

---

## 🚀 Features

* Create payments with **Idempotency‑Key** support
* Retrieve payment details by ID
* Explicit payment lifecycle actions:

  * Confirm payment
  * Fail payment
  * Refund payment
* Clear payment state transitions
* PostgreSQL persistence
* OpenAPI / Swagger documentation
* Docker & docker‑compose ready

---

## 🧠 Payment Lifecycle

Each payment goes through well‑defined states:

```
pending → confirmed
pending → failed
confirmed → refunded
```

Invalid transitions are rejected to keep data consistent and predictable.

---

## 📦 Tech Stack

* **Python 3.11**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Uvicorn**
* **Docker / Docker Compose**

---

## 📂 Project Structure

```bash
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 27d6eaa1b56e_add_idempotency_key.py
│       └── a6cc2dc342a4_create_payments_table.py
├── alembic.ini
├── app
│   ├── api
│   │   ├── __init__.py
│   │   └── routers
│   │       ├── health.py
│   │       └── payments.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── db.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── payment.py
│   ├── schemas
│   │   ├──  __init__.py
│   │   └── payment.py
│   └── services
│       ├── __init__.py
│       └── payments.py
├── commands.txt
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── structure.txt
└── test
    ├── conftest.py
    ├──  __init__.py
    ├── test_health.py
    ├── test_idempotency.py
    ├── test_payments_flow.py
    ├── test_payments.py
    └── utils.py


```

## 🔌 API Endpoints

### Health Check

```
GET /health
```

Returns service status.

---

### Create Payment

```
POST /api/v1/payments/
```

**Headers**

```
Idempotency-Key: unique-key
```

**Request body**

```json
{
  "order_id": 1,
  "amount": 10.00,
  "currency": "USD"
}
```

**Response**

* `201 Created` — new payment created
* `200 OK` — idempotent request retry

---

### Get Payment

```
GET /api/v1/payments/{payment_id}
```

---

### Confirm Payment

```
POST /api/v1/payments/{payment_id}/confirm
```

---

### Fail Payment

```
POST /api/v1/payments/{payment_id}/fail
```

---

### Refund Payment

```
POST /api/v1/payments/{payment_id}/refund
```

---

## 🔄 Example API Flows

This section demonstrates typical real-world usage scenarios of the Payment Service API.

### 🟢 Flow 1: Successful Payment

1. Create a payment

```http
POST /api/v1/payments/
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000
```
**Request body**
```json
{
  "order_id": 42,
  "amount": 99.99,
  "currency": "USD"
}
```

**Response — 201 Created**
```json
{
  "id": 1,
  "order_id": 42,
  "amount": 99.99,
  "currency": "USD",
  "status": "pending",
  "provider": "internal",
  "created_at": "2026-01-16T16:57:41.614Z",
  "updated_at": "2026-01-16T16:57:41.614Z"
}
```

2. Confirm the payment

```http
POST /api/v1/payments/1/confirm
```

**Response — 200 OK**
```json
{
  "id": 1,
  "status": "confirmed",
  "updated_at": "2026-01-16T16:58:10.075Z"
}
```

✅ Payment successfully completed.

### 🔁 Flow 2: Idempotent Request Retry

A client retries the same payment creation request (e.g. network timeout).

```http
POST /api/v1/payments/
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000
```
**Request body**
```json
{
  "order_id": 42,
  "amount": 99.99,
  "currency": "USD"
}
```

**Response — 200 OK**
```json
{
  "id": 1,
  "status": "pending"
}
```

🔒 No duplicate payment created — the existing payment is safely returned.

### 🔴 Flow 3: Failed Payment

1. Create a payment → status pending

2. Mark payment as failed

```http
POST /api/v1/payments/2/fail
```

**Response**
```json
{
  "id": 2,
  "status": "failed"
}
```

❌ Payment failed and cannot be confirmed or refunded afterwards.

### 💸 Flow 4: Refund a Confirmed Payment

1. Create payment → pending
2. Confirm payment → confirmed

3. Refund payment

```http
POST /api/v1/payments/3/refund
```

**Response**
```json
{
  "id": 3,
  "status": "refunded"
}
```

💰 Funds successfully refunded.

### ⚠️ Flow 5: Invalid State Transition

Attempt to refund a payment that is still pending:

```http
POST /api/v1/payments/4/refund
```

**Response — 409 Conflict**
```json
{
  "detail": "Cannot refund payment in pending status"
}
```

🚫 Business rules are strictly enforced to guarantee data consistency.

🧠 Why This Matters

These flows demonstrate:

- Idempotent payment creation
- Explicit state transitions
- Predictable business rules
- Safe retries in distributed systems
- Clear error handling

This mirrors how real payment services behave in production environments.

---

## 🧪 Testing

All endpoints are fully testable via:

* Swagger UI (`/docs`)
* curl / HTTP clients

Idempotency behavior and state changes are verified via logs and database state.

---

## 🔁 Idempotency

Payment creation supports idempotent requests via the `Idempotency-Key` header.

Rules:
- Repeating the same request with the same key returns the existing payment (`200 OK`)
- Reusing the same key with different payload returns `409 Conflict`
- Guarantees safe retries in distributed systems

---

## ⚠️ Error Handling

The API uses standard HTTP status codes:

- `400` — invalid request / business rule violation
- `404` — payment not found
- `409` — idempotency conflict or invalid state transition
- `422` — validation errors

All errors return a structured JSON response.

---

## 🧪 Test Coverage

The project includes full async test coverage:

- Payment creation & retrieval
- Idempotency scenarios
- Valid and invalid state transitions
- Refund / confirm / fail flows
- Non-existent resource handling

Tests are implemented using `pytest` and `httpx.AsyncClient`.

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

Service will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## 📈 Project Purpose

This project is part of a backend portfolio and demonstrates:

* API design best practices
* Payment domain modeling
* State‑driven business logic
* Production‑ready structure

It can be easily integrated with an **Order Service** or extended with real payment providers.

---

## 👤 Author

**๛Samer Shams๖**
- Backend Developer (Python / FastAPI)

## 📢 **Contacts**

- **Email**: sammertime763@gmail.com

- **Telegram**: [Mr_Shams_1986](https://t.me/Mr_Shams_1986)

---

## 📄 License

MIT License
