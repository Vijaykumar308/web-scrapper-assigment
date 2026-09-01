"""Export the shared product model to download-friendly formats."""

import csv
import io
import json
from collections.abc import Sequence

from .models import Product


def to_csv(products: Sequence[Product]) -> bytes:
    output = io.StringIO()
    fields = list(Product.model_fields)
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for product in products:
        writer.writerow(product.model_dump(mode="json"))
    return output.getvalue().encode("utf-8")


def to_json(products: Sequence[Product]) -> bytes:
    return json.dumps([product.model_dump(mode="json") for product in products], indent=2).encode("utf-8")


def to_xlsx(products: Sequence[Product]) -> bytes:
    from openpyxl import Workbook

    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    fields = list(Product.model_fields)
    sheet.append(fields)
    for product in products:
        row = product.model_dump(mode="json")
        sheet.append([row[field] for field in fields])
    output = io.BytesIO()
    workbook.save(output)
    return output.getvalue()
