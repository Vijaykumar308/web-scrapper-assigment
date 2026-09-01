"""Location lookup and delivery-location abstraction."""

from .config import CITY_PINCODES
from .exceptions import LocationSetError


def resolve_pincode(city: str) -> str:
    normalized = city.strip().casefold()
    for known_city, pincode in CITY_PINCODES.items():
        if known_city.casefold() == normalized:
            return pincode
    raise LocationSetError(f"Unsupported city: {city}")


def set_delivery_location(page: object, city: str) -> str:
    """Resolve a city before browser interaction; adapters can apply the pincode."""
    return resolve_pincode(city)
