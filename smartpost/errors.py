from __future__ import annotations

from typing import Any

errors_explanation: dict[str, str] = {
    "000": "Destination info missing",
    "001": "Required input missing",
    "002": "Barcode already exists",
    "003": "Not a phone number",
    "004": "Not an e-mail address",
    "005": "Not numeric",
    "006": "Unknown destination (place_id)",
    "007": "Express checked but destination is not a express APT",
    "008": "Multiple destinations set",
    "009": "Courier service timeframe missing",
    "010": "Courier service city missing",
    "011": "Courier service postal code missing",
    "012": "Courier address missing",
    "013": "COD used but service not available",
    "014": "Invalid door size",
    "015": "String too long (LQ items)",
    "016": "Integer out of bounds (LQ items)",
    "017": "Value not in enum list (LQ items)",
    "018": "Sending with door code service not activated",
}


class ShipmentOrderErrorDetails:
    """Additional details about shipment order with issues."""

    def __init__(self, item: dict[str, Any]) -> None:
        self.barcode: str | None = item.get("barcode")
        self.reference: str | None = item.get("reference")
        self.code: str = item.get("code", "")
        self.text: str = item.get("text", "")
        self.input: str | None = item.get("input")
        if self.barcode is not None:
            error = item["error"]
            self.code = error["code"]
            self.text = error["text"]
            self.input = error.get("input")

        self.message: str = errors_explanation[self.code]

    def __str__(self) -> str:
        return (
            f"ShipmentOrderErrorDetails(barcode={self.barcode}, "
            f"reference={self.reference}, code={self.code}, message={self.message}, "
            f"text={self.text}, input={self.input})"
        )

    __repr__ = __str__


class ShipmentOrderError(Exception):
    """Error that is raised when there are issues with shipment orders."""

    def __init__(self, errors: dict[str, Any]) -> None:
        self.errors: list[ShipmentOrderErrorDetails] = [
            ShipmentOrderErrorDetails(item) for item in errors["item"]
        ]


class ShipmentLabelsError(Exception):  # noqa: B903
    """Error that is raised when there are issues with shipment labels (PDF)."""

    def __init__(self, body: bytes, status_code: int) -> None:
        self.body = body
        self.status_code = status_code
