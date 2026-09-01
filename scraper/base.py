"""Base contract and resilient execution helpers for platform scrapers."""

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any
from urllib.parse import urljoin

from .config import ScraperConfig
from .exceptions import ParseError
from .models import Product
from .validators import clean_price, clean_text

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(self, city: str, config: ScraperConfig | None = None) -> None:
        self.city = city
        self.config = config or ScraperConfig()
        self.query = ""

    @abstractmethod
    def set_location(self, city: str) -> None: ...

    @abstractmethod
    def search(self, query: str) -> None: ...

    @abstractmethod
    def extract_products(self) -> list[Product]: ...

    def run(self, query: str) -> list[Product]:
        self.set_location(self.city)
        self.search(query)
        return self.extract_products()

    def retry(self, operation: Callable[[], Any]) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.config.retries):
            try:
                return operation()
            except Exception as error:
                last_error = error
                if attempt + 1 < self.config.retries:
                    time.sleep(self.config.retry_backoff_seconds * (attempt + 1))
        raise RuntimeError("operation failed after retries") from last_error

    def browser(self) -> Any:
        """Create a browser context lazily so importing the package stays lightweight."""
        from playwright.sync_api import sync_playwright

        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=self.config.headless, timeout=self.config.timeout_ms)
        context = browser.new_context(
            locale="en-IN",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
        )
        return playwright, browser, context

    def prepare_page(self, page: Any) -> Any:
        page.set_default_timeout(self.config.timeout_ms)
        page.set_default_navigation_timeout(self.config.timeout_ms)
        return page

    @staticmethod
    def absolute_url(url: str, base_url: str) -> str:
        return urljoin(base_url, url)

    @staticmethod
    def product_from_payload(payload: dict[str, Any], platform: str, city: str) -> Product:
        try:
            return Product(
                product_name=clean_text(payload.get("product_name")) or "Unknown product",
                brand=clean_text(payload.get("brand")),
                selling_price=clean_price(payload.get("selling_price")),
                mrp=clean_price(payload.get("mrp")),
                discount=clean_price(payload.get("discount")),
                availability=clean_text(payload.get("availability")),
                product_url=clean_text(payload.get("product_url")),
                category=clean_text(payload.get("category")),
                subcategory=clean_text(payload.get("subcategory")),
                pack_size=clean_text(payload.get("pack_size")),
                platform=platform,
                city=city,
            )
        except Exception as error:
            raise ParseError(f"Unable to parse product payload: {payload}") from error
