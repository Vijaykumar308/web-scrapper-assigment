"""Blinkit adapter. Browser hooks are isolated so selectors can evolve independently."""

import logging
import time
from typing import Any
from urllib.parse import quote_plus

from .base import BaseScraper
from .config import CITY_PINCODES
from .models import Product
from .exceptions import ScraperError
from .validators import clean_price, clean_text, slugify

logger = logging.getLogger(__name__)


class BlinkitScraper(BaseScraper):
    platform = "blinkit"

    def set_location(self, city: str) -> None:
        if city not in CITY_PINCODES:
            from .location import resolve_pincode
            resolve_pincode(city)
        self.city = city
        self.pincode = CITY_PINCODES[city]

    def search(self, query: str) -> None:
        self.query = query.strip()
        time.sleep(self.config.request_delay_seconds)

    def extract_products(self) -> list[Product]:
        url = f"https://blinkit.com/s/?q={quote_plus(self.query)}"
        playwright, browser, context = self.browser()
        try:
            page = self.prepare_page(context.new_page())
            response = page.goto(url, wait_until="commit", timeout=self.config.timeout_ms)
            page.wait_for_timeout(2500)
            if response is not None and response.status >= 400:
                raise ScraperError(f"Blinkit returned HTTP {response.status}")
            self._apply_location(page)
            page.wait_for_timeout(1500)
            records = page.locator("div[role='button'][id]").evaluate_all("""cards => cards.map(card => {
                const name = card.querySelector('[class*="line-clamp-2"]')?.innerText || '';
                const pack = card.querySelector('[class*="line-clamp-1"]')?.innerText || '';
                const prices = [...card.querySelectorAll('div')].map(node => node.innerText.trim())
                    .filter(value => /^₹[\\d,]+(?:\\.\\d+)?$/.test(value));
                return { id: card.id, name, pack, prices, text: card.innerText };
            }).filter(item => /^\\d+$/.test(item.id) && item.name.trim())""")
            products = self._products_from_records(records)
            if not products:
                raise ScraperError("Blinkit returned no product detail links; location or anti-bot verification may be required")
            return products
        except Exception as error:
            raise ScraperError(f"Blinkit extraction failed: {error}") from error
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def _apply_location(self, page: Any) -> None:
        """Dismiss Blinkit's location gate when the page exposes a pincode field."""
        for selector in ("input[placeholder*='pincode' i]", "input[placeholder*='location' i]", "input[type='text']"):
            field = page.locator(selector).first
            if field.count() == 0:
                continue
            try:
                field.fill(self.pincode)
                field.press("Enter")
                return
            except Exception:
                continue

    def _products_from_records(self, records: list[dict[str, Any]]) -> list[Product]:
        products: list[Product] = []
        seen: set[str] = set()
        for record in records:
            name = clean_text(record.get("name")) or self.query
            product_id = clean_text(record.get("id"))
            if not product_id:
                continue
            url = f"https://blinkit.com/prn/{slugify(name)}/prid/{product_id}"
            if url in seen:
                continue
            seen.add(url)
            products.append(self.product_from_payload({
                "product_name": name,
                "selling_price": clean_price((record.get("prices") or [None])[0]),
                "mrp": clean_price((record.get("prices") or [None, None])[1]),
                "availability": "In stock",
                "pack_size": clean_text(record.get("pack")),
                "product_url": url,
            }, self.platform, self.city))
        return products
