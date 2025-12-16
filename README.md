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
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
└── structure.txt

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
* `200 OK` — idempotent повтор запроса

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

## 🧪 Testing

All endpoints are fully testable via:

* Swagger UI (`/docs`)
* curl / HTTP clients

Idempotency behavior and state changes are verified via logs and database state.

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
Backend Developer (Python / FastAPI)

---

## 📄 License

MIT License
