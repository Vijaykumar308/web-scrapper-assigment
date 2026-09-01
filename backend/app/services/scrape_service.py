import logging
from uuid import UUID

from scraper.bigbasket_scraper import BigBasketScraper
from scraper.blinkit_scraper import BlinkitScraper
from scraper.models import Product

from app.jobs.job_store import JobStore
from app.schemas.scrape import ScrapeRequest

logger = logging.getLogger(__name__)


class ScrapeService:
    def __init__(self, store: JobStore) -> None:
        self.store = store

    def run(self, job_id: UUID, request: ScrapeRequest) -> None:
        self.store.update(job_id, status="running", progress=5)
        try:
            scraper_types = {
                "blinkit": BlinkitScraper,
                "bigbasket": BigBasketScraper,
            }
            platforms = [request.platform] if request.platform != "both" else ["blinkit", "bigbasket"]
            products: list[Product] = []
            for index, platform in enumerate(platforms):
                scraper = scraper_types[platform](request.city)
                products.extend(scraper.run(request.query))
                self.store.update(job_id, progress=5 + int((index + 1) / len(platforms) * 90))
            self.store.update(job_id, status="done", progress=100, products=products)
        except Exception as error:
            logger.exception("Scrape job %s failed", job_id)
            self.store.update(job_id, status="failed", error=str(error))
