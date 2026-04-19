# Venerable Vault API

A FastAPI-based REST API for managing antique items, tracking provenance history, and calculating valuations.

## Overview

The Venerable Vault API provides a complete system for antique dealers, collectors, and appraisers to:

- Catalog antique items with detailed attributes
- Track provenance (ownership history, restorations, appraisals)
- Calculate automated valuations based on age, condition, and documentation

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Server                          │
│                      (app/main.py:1)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
     ┌────────────────┐ ┌──────────┐ ┌────────────────┐
     │  Routes Layer  │ │  CRUD    │ │  Valuation     │
     │ items.py:1     │ │ crud.py  │ │ valuation.py   │
     └────────────────┘ └──────────┘ └────────────────┘
              │               │
              ▼               ▼
     ┌────────────────────────────────────────┐
     │            Models Layer                │
     │         (app/models.py:1)              │
     │  Item │ ProvenanceEvent │ Valuation    │
     └────────────────────────────────────────┘
                              │
                              ▼
     ┌────────────────────────────────────────┐
     │          Database (SQLite)             │
     │           vault.db                     │
     │  items │ provenance_events │ valuations│
     └────────────────────────────────────────┘
```

## Data Model

```
┌──────────────────────────────────────────────────────────────────────┐
│                           ITEM                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ id: Integer (PK)                                              │  │
│  │ name: String                                                  │  │
│  │ base_cost: Float                                              │  │
│  │ age_category: String (antique/vintage/modern/contemporary)   │  │
│  │ documents_count: Integer                                      │  │
│  │ created_at: DateTime                                          │  │
│  │ updated_at: DateTime                                          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              │ 1:N                                   │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    PROVENANCE_EVENT                            │  │
│  │  id: Integer (PK)                                             │  │
│  │  description: String                                          │  │
│  │  year: Integer                                                │  │
│  │  event_type: String (restoration/appraisal/ownership)         │  │
│  │  documented: Boolean                                          │  │
│  │  item_id: Integer (FK → Item.id)                              │  │
│  │  created_at: DateTime                                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              │ N:1 (optional)                       │
│                              ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                      VALUATION                                 │  │
│  │  id: Integer (PK)                                             │  │
│  │  calculated_value: Float                                      │  │
│  │  multiplier_used: Float                                       │  │
│  │  notes: String (optional)                                     │  │
│  │  item_id: Integer (FK → Item.id)                              │  │
│  │  created_at: DateTime                                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

## API Endpoints

### Items

| Method   | Endpoint          | Description                    |
| -------- | ----------------- | ------------------------------ |
| `POST`   | `/api/items/`     | Create a new item              |
| `GET`    | `/api/items/`     | List all items                 |
| `GET`    | `/api/items/{id}` | Get item by ID with provenance |
| `DELETE` | `/api/items/{id}` | Delete an item                 |

### Provenance

| Method | Endpoint                      | Description               |
| ------ | ----------------------------- | ------------------------- |
| `POST` | `/api/items/{id}/provenance/` | Add provenance event      |
| `GET`  | `/api/items/{id}/provenance/` | Get all provenance events |

### Valuation

| Method | Endpoint                      | Description           |
| ------ | ----------------------------- | --------------------- |
| `GET`  | `/api/items/{id}/valuation/`  | Get current valuation |
| `GET`  | `/api/items/{id}/valuations/` | Get valuation history |

## Valuation Logic

The valuation engine calculates value using:

```
base_value × age_multiplier × documentation_bonus
```

**Age Multipliers:**
| Category | Multiplier |
|----------|------------|
| antique | +1.5 |
| vintage | +1.2 |
| modern | +1.0 |
| contemporary | +0.9 |

**Documentation Bonus:**
| Documents | Bonus |
|-----------|-------|
| 5+ | +0.5 |
| 3-4 | +0.3 |
| 1-2 | +0.1 |

**Example:**

- Base cost: $5000
- Age: antique (+1.5) → multiplier = 2.5
- 3 provenance events (+0.3) → multiplier = 2.8
- **Final Value**: $5000 × 2.8 = **$14,000**

## Setup & Installation

### Prerequisites

- Python 3.11+
- SQLite

### Installation

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run HTTP Client tests in PyCharm
# Right-click tests/api_test.http → Run HTTP Client

# Or use pytest
pytest tests/
```

## API Documentation

Once running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## Example Usage

### Create an Item

```bash
curl -X POST http://127.0.0.1:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "18th Century Writing Desk",
    "base_cost": 5000,
    "age_category": "antique",
    "documents_count": 0
  }'
```

### Add Provenance Event

```bash
curl -X POST http://127.0.0.1:8000/api/items/1/provenance/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Refinished mahogany surface",
    "year": 1995,
    "event_type": "restoration",
    "documented": true
  }'
```

### Get Valuation

```bash
curl http://127.0.0.1:8000/api/items/1/valuation/
```

Response:

```json
{
  "item_id": 1,
  "item_name": "18th Century Writing Desk",
  "base_cost": 5000.0,
  "age_category": "antique",
  "provenance_events_count": 3,
  "valuation": 14000.0,
  "multiplier_used": 2.8
}
```

## Project Structure

```
venerable_vault_api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # Database operations
│   ├── database.py       # DB connection
│   ├── valuation.py      # Valuation logic
│   └── routes/
│       ├── __init__.py
│       └── items.py      # API endpoints
├── tests/
│   └── api_test.http     # PyCharm HTTP tests
├── vault.db              # SQLite database
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Debugging in PyCharm

1. **Set Breakpoints**: Click in the gutter next to line numbers in:
   - `app/routes/items.py` - API route handlers
   - `app/crud.py` - Database operations
   - `app/valuation.py` - Valuation calculation

2. **Debug HTTP Requests**:
   - Right-click `tests/api_test.http`
   - Select "Debug HTTP Client"

3. **Run with Debugger**:
   - Click the debug icon next to the run configuration
   - Or press `Shift+F9` after setting breakpoints

## License

MIT
