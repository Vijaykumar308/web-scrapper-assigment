from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import Response

from app.schemas.scrape import ProductResponse, ResultsResponse

router = APIRouter(prefix="/api/results", tags=["results"])


@router.get("/{job_id}", response_model=ResultsResponse)
def get_results(job_id: UUID, request: Request, page: int = Query(1, ge=1), page_size: int = Query(25, ge=1, le=100)) -> ResultsResponse:
    job = request.app.state.scrape_service.store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    start = (page - 1) * page_size
    items = [ProductResponse(**product.model_dump(mode="json")) for product in job.products[start:start + page_size]]
    return ResultsResponse(items=items, page=page, page_size=page_size, total=len(job.products))


@router.get("/{job_id}/download")
def download_results(job_id: UUID, request: Request, format: Literal["csv", "json", "xlsx"] = "csv") -> Response:
    job = request.app.state.scrape_service.store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    content, media_type = request.app.state.export_service.export(job.products, format)
    return Response(content=content, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="products-{job_id}.{format}"'})
