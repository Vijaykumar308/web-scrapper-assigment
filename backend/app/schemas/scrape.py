from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


Platform = Literal["blinkit", "bigbasket", "both"]


class ScrapeRequest(BaseModel):
    platform: Platform
    city: str = Field(min_length=2, max_length=50)
    query: str = Field(min_length=1, max_length=120)


class ScrapeCreated(BaseModel):
    job_id: UUID


class JobStatusResponse(BaseModel):
    job_id: UUID
    status: Literal["pending", "running", "done", "failed"]
    progress: int = Field(ge=0, le=100)
    error: str | None = None


class ProductResponse(BaseModel):
    product_name: str
    brand: str | None = None
    selling_price: float | None = None
    mrp: float | None = None
    discount: float | None = None
    availability: str | None = None
    product_url: str | None = None
    category: str | None = None
    subcategory: str | None = None
    pack_size: str | None = None
    platform: str
    city: str
    scraped_at: str


class ResultsResponse(BaseModel):
    items: list[ProductResponse]
    page: int
    page_size: int
    total: int
