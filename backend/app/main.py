from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes_results import router as results_router
from app.api.routes_scrape import router as scrape_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.jobs.job_store import JobStore
from app.services.export_service import ExportService
from app.services.scrape_service import ScrapeService

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app_name)
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_methods=["*"], allow_headers=["*"])
app.state.scrape_service = ScrapeService(JobStore())
app.state.export_service = ExportService()
app.include_router(scrape_router)
app.include_router(results_router)


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": {"code": "internal_error", "message": "An unexpected error occurred"}})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
