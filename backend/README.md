# Adhikar Setu - Backend API

This directory contains the FastAPI backend service for **Adhikar Setu**, an AI-powered personalized government scheme information and recommendation system.

---

## 📁 Directory Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entrypoint & FastAPI initialization
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Centralized app configuration & settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py    # Versioned API routes & health check endpoint
│   ├── schemas/             # Request & response Pydantic schemas (Future)
│   ├── models/              # Database models (Future)
│   ├── database/            # Database connection & session handlers (Future)
│   ├── repositories/        # Data access layer (Future)
│   ├── services/            # Business logic & scheme matching services (Future)
│   ├── ai/                  # RAG, LLM, & Vector Search integrations (Future)
│   └── tests/               # Backend unit and integration tests (Future)
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules for backend
├── requirements.txt         # Minimum Python dependencies
└── README.md                # Backend documentation
```

---

## 🛠️ Setup & Installation

### 1. Create and Activate Virtual Environment

From the `backend` directory:

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Copy `.env.example` to create a local `.env` file:

```bash
cp .env.example .env
```

---

## 🚀 Running the Application

To run the backend server locally with hot-reloading:

### Option A: From Repository Root
```bash
uvicorn app.main:app --reload --app-dir backend
```

### Option B: From `backend` Directory
```bash
cd backend
uvicorn app.main:app --reload
```

---

## 🌐 Interactive API Documentation

Once the server is running, you can access:

* **Root Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
* **Interactive API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
