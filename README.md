# Secure Log Analysis API

A REST API for ingesting, storing, and querying application log data, built in Python with FastAPI. It exposes clean, validated endpoints for submitting log entries — individually or in batches — and retrieving them with flexible filtering, following a secure-by-design approach inspired by tools like Splunk and Datadog.

> **Status:** Actively developed. Uses synthetic data only — no real or sensitive information.

---

## Features

- **Structured log ingestion** — submit single entries or batches over a REST API
- **Flexible querying** — filter stored logs by level and time range
- **Automatic validation** — every request is validated against a typed schema (Pydantic)
- **Interactive API docs** — Swagger UI generated automatically by FastAPI
- **Secure-by-design** — input validation today, with a clear path to authentication, persistence, and hardening (see [Security](#security))

## Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python 3.12 |
| Framework | FastAPI |
| Validation | Pydantic |
| Server | Uvicorn (ASGI) |

## API Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/upload` | Submit a single log entry |
| `POST` | `/upload/batch` | Submit multiple log entries |
| `GET` | `/logs` | Retrieve logs, with optional `level`, `start`, and `end` filters |

**Log entry schema**

```json
{
  "timestamp": "2026-06-21T10:30:00",
  "level": "ERROR",
  "message": "Database connection timed out"
}
```

**Submit a log entry**

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"timestamp": "2026-06-21T10:30:00", "level": "ERROR", "message": "Database connection timed out"}'
```

**Query logs by level**

```bash
curl "http://127.0.0.1:8000/logs?level=ERROR"
```

**Response**

```json
{
  "count": 1,
  "logs": [
    {
      "timestamp": "2026-06-21T10:30:00",
      "level": "ERROR",
      "message": "Database connection timed out"
    }
  ]
}
```

## Getting Started

```bash
# Clone the repository
git clone https://github.com/NickolasAM/secure-log-analysis-api.git
cd secure-log-analysis-api

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload
```

Once running:

- API base URL: `http://127.0.0.1:8000`
- Interactive documentation: `http://127.0.0.1:8000/docs`

## Security

Security is treated as a first-class concern in this project, not an afterthought.

**Implemented**
- Strict request validation on all incoming data via typed Pydantic models
- Secrets and environment files kept out of version control (`.gitignore`)

**Planned**
- API key / token authentication on all endpoints
- Request size and input limits to prevent abuse
- Parameterized SQL queries to prevent injection (introduced with the database layer)
- Access logging and clean error handling that avoids leaking internal details
- HTTPS/TLS for any production deployment

## Roadmap

- **Phase A — Core API** *(in progress):* ingestion and query endpoints, validation, filtering, keyword search, pagination
- **Phase B — Persistence:** SQLite, then PostgreSQL; filters rewritten as parameterized queries; a statistics endpoint
- **Phase C — Containerization:** Docker packaging, documentation, and polish
- **Cross-cutting:** automated tests (pytest) and the security items above, added alongside each phase

> **Note:** Storage is currently in-memory and resets on restart; database-backed persistence arrives in Phase B.

## About

I built this to learn backend development properly and to have a real, working project that demonstrates what I can do — not just tutorial code. Through it I've become comfortable with FastAPI and gained a clearer understanding of how APIs work under the hood. I'm building it with security in mind from the start, because I want to demonstrate the mindset of thinking about how an application is protected — not just making it run.

