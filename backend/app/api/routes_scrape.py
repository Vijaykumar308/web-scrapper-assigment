from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from app.schemas.scrape import JobStatusResponse, ScrapeCreated, ScrapeRequest
from app.services.scrape_service import ScrapeService

router = APIRouter(prefix="/api/scrape", tags=["scrape"])


def service(request: Request) -> ScrapeService:
    return request.app.state.scrape_service


@router.post("", response_model=ScrapeCreated, status_code=status.HTTP_202_ACCEPTED)
def create_scrape(payload: ScrapeRequest, background_tasks: BackgroundTasks, request: Request) -> ScrapeCreated:
    job = service(request).store.create()
    background_tasks.add_task(service(request).run, job.job_id, payload)
    return ScrapeCreated(job_id=job.job_id)


@router.get("/{job_id}/status", response_model=JobStatusResponse)
def get_status(job_id: UUID, request: Request) -> JobStatusResponse:
    job = service(request).store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job.job_id, status=job.status, progress=job.progress, error=job.error)
