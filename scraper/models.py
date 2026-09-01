"""Shared product contract."""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")

    product_name: str
    brand: str | None = None
    selling_price: float | None = Field(default=None, ge=0)
    mrp: float | None = Field(default=None, ge=0)
    discount: float | None = Field(default=None, ge=0, le=100)
    availability: str | None = None
    product_url: str | None = None
    category: str | None = None
    subcategory: str | None = None
    pack_size: str | None = None
    platform: str
    city: str
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("product_name", "platform", "city")
    @classmethod
    def required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text field cannot be empty")
        return cleaned

    @model_validator(mode="after")
    def calculate_discount(self) -> "Product":
        if self.discount is None and self.mrp and self.selling_price is not None:
            self.discount = round(max(0, (self.mrp - self.selling_price) / self.mrp * 100), 2)
        return self

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
