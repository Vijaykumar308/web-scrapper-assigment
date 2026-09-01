from collections.abc import Sequence

from scraper import exporters
from scraper.models import Product


class ExportService:
    _content_types = {
        "csv": "text/csv",
        "json": "application/json",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    def export(self, products: Sequence[Product], file_format: str) -> tuple[bytes, str]:
        functions = {"csv": exporters.to_csv, "json": exporters.to_json, "xlsx": exporters.to_xlsx}
        if file_format not in functions:
            raise ValueError("format must be csv, json, or xlsx")
        return functions[file_format](products), self._content_types[file_format]
