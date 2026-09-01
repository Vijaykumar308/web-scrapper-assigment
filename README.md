# Retail Radar

A modular Blinkit and BigBasket product listing scraper with a FastAPI job API and React + TypeScript dashboard.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Install the browser used by the live adapters:
python -m playwright install chromium

# Optional: use a visible browser when a retailer presents an anti-bot or location gate.
$env:SCRAPER_HEADLESS = "false"
```

Start the backend from the repository root:

```powershell
uvicorn app.main:app --app-dir backend --reload
```

Start the frontend in another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL, usually `http://localhost:5173`. Submit a platform, city, and query. The UI polls the background job, renders results, and downloads CSV, JSON, or XLSX from the API.

## Design notes

`BaseScraper` is the platform contract. City validation and pincode mapping live in `scraper/config.py`. Each adapter uses Playwright and extracts the product name, prices, and exact product-detail URL from the same live listing card. A parse error affects only its product payload, while job-level failures are recorded in the job store. Retailer anti-bot pages or location gates are reported as failed jobs rather than replaced with made-up product data.

The in-memory job store is intentionally simple for this assignment. Production deployment should move job state and result storage to Redis/PostgreSQL or object storage, and use a worker queue instead of process-local background tasks.
