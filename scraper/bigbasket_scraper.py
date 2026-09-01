"""BigBasket adapter with the same contract as every future platform."""

import time
from typing import Any
from urllib.parse import quote_plus

from .base import BaseScraper
from .config import CITY_PINCODES
from .models import Product
from .exceptions import ScraperError


class BigBasketScraper(BaseScraper):
    platform = "bigbasket"

    def set_location(self, city: str) -> None:
        from .location import resolve_pincode
        self.pincode = resolve_pincode(city)
        self.city = city

    def search(self, query: str) -> None:
        self.query = query.strip()
        time.sleep(self.config.request_delay_seconds)

    def extract_products(self) -> list[Product]:
        url = f"https://www.bigbasket.com/ps/?q={quote_plus(self.query)}"
        playwright, browser, context = self.browser()
        try:
            page = self.prepare_page(context.new_page())
            response = page.goto(url, wait_until="commit", timeout=self.config.timeout_ms)
            page.wait_for_timeout(2500)
            if response is not None and response.status >= 400:
                raise ScraperError(f"BigBasket returned HTTP {response.status}; the site blocked this request")
            records = page.locator("a[href]").evaluate_all("""anchors => anchors.map(anchor => {
                const href = anchor.href;
                const text = anchor.closest('li, article, [data-testid], div')?.innerText || anchor.innerText || '';
                return { href, text };
            }).filter(item => /bigbasket.com\/pd\//.test(item.href) && item.text.trim().length > 10)""")
            products = self._products_from_records(records)
            if not products:
                raise ScraperError("BigBasket returned no product detail links; location or anti-bot verification may be required")
            return products
        except Exception as error:
            raise ScraperError(f"BigBasket extraction failed: {error}") from error
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def _products_from_records(self, records: list[dict[str, Any]]) -> list[Product]:
        import re

        products: list[Product] = []
        seen: set[str] = set()
        for record in records:
            url = str(record.get("href", ""))
            if url in seen:
                continue
            seen.add(url)
            text = " ".join(str(record.get("text", "")).split())
            prices = re.findall(r"(?:₹|Rs\.?\s*)\s*([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
            product_name = re.split(r"(?:₹|Rs\.?\s*)", text, maxsplit=1, flags=re.IGNORECASE)[0].strip()[:200]
            products.append(self.product_from_payload({
                "product_name": product_name or self.query,
                "selling_price": prices[0] if prices else None,
                "mrp": prices[1] if len(prices) > 1 else None,
                "availability": "In stock",
                "product_url": url,
            }, self.platform, self.city))
        return products
