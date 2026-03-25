# NER Project: Backend + Frontend Setup Guide

This guide explains how to run the full project locally, including:
- Creating a Python virtual environment
- Installing backend and frontend dependencies
- Configuring environment variables
- Running backend and frontend together

## 1. Prerequisites

Install these first:
- Python 3.11+
- Node.js 18+ and npm
- Git (optional, for cloning)

Check versions:

```bash
python3 --version
node --version
npm --version
```

## 2. Clone / Open Project

If you already have the project, skip this section.

```bash
git clone <your-repo-url>
cd ner
```

## 3. Backend Setup (FastAPI)

From the project root:

```bash
cd backend
```

### 3.1 Create virtual environment

```bash
python3 -m venv ../.venv
```

### 3.2 Activate virtual environment

Linux/macOS:

```bash
source ../.venv/bin/activate
```

Windows (PowerShell):

```powershell
..\.venv\Scripts\Activate.ps1
```

### 3.3 Upgrade pip and install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment Variables (for LangExtract endpoint)

The backend loads variables from:

- `backend/.env`

Create the file `backend/.env` if it does not exist, then add:

```env
LANGEXTRACT_API_KEY=your_api_key_here
```

Notes:
- This is required for `/langextract` and `/analyze-all` when LangExtract is used.
- `/convert-pdf`, `/ner`, and `/sentiment` can still run without this key.

## 5. Run Backend API

From `backend` directory (with virtual environment active):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

## 6. Frontend Setup (React + Vite)

Open a new terminal and go to frontend folder from project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend will run at:
- `http://localhost:3000`

The frontend is already configured to proxy API requests to the backend at `http://localhost:8000`.

## 7. Run Both Together (Recommended Workflow)

Use two terminals:

Terminal 1 (backend):

```bash
cd backend
source ../.venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (frontend):

```bash
cd frontend
npm install
npm run dev
```

Then open:

- Frontend app: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

## 8. Common Issues

### 8.1 `ModuleNotFoundError` in backend

Cause: virtual environment not activated or dependencies not installed.

Fix:

```bash
cd backend
source ../.venv/bin/activate
pip install -r requirements.txt
```

### 8.2 Frontend cannot reach backend

Make sure backend is running on port 8000:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

### 8.3 LangExtract endpoint fails

Check that `backend/.env` exists and contains a valid key:

```env
LANGEXTRACT_API_KEY=your_api_key_here
```

## 9. Stop Services

In each terminal, press `Ctrl + C`.

If you want to deactivate the Python virtual environment:

```bash
deactivate
```
