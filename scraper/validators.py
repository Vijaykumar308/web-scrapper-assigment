"""Small normalization helpers shared by platform adapters."""

import re
from urllib.parse import quote_plus
from typing import Any


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def clean_price(value: Any) -> float | None:
    if value is None:
        return None
    match = re.search(r"\d[\d,]*(?:\.\d+)?", str(value))
    if not match:
        return None
    try:
        return float(match.group(0).replace(",", ""))
    except ValueError:
        return None


def slugify(value: str) -> str:
    """Create a stable URL segment for normalized product names."""
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def retailer_search_url(platform: str, product_name: str) -> str:
    query = quote_plus(product_name)
    if platform == "blinkit":
        return f"https://blinkit.com/s/?q={query}"
    return f"https://www.bigbasket.com/ps/?q={query}"
