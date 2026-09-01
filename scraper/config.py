"""Runtime configuration and supported delivery locations."""

import os
from dataclasses import dataclass

CITY_PINCODES: dict[str, str] = {
    "Gurgaon": "122001",
    "Mumbai": "400001",
    "Delhi": "110001",
    "Bengaluru": "560001",
    "Hyderabad": "500001",
    "Pune": "411001",
    "Chennai": "600001",
    "Kolkata": "700001",
}


@dataclass(frozen=True)
class ScraperConfig:
    timeout_ms: int = 12_000
    retries: int = 1
    retry_backoff_seconds: float = 0.5
    request_delay_seconds: float = 0.25
    # Retailer anti-bot pages commonly reject headless Chromium during local runs.
    headless: bool = os.getenv("SCRAPER_HEADLESS", "false").casefold() == "true"
