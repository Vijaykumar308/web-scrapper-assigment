class ScraperError(Exception):
    """Base exception for scraper failures."""


class LocationSetError(ScraperError):
    """Raised when a supported delivery location cannot be applied."""


class ParseError(ScraperError):
    """Raised when a product payload cannot be normalized."""
