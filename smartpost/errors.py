from typing import Any, Dict, List, Optional

errors_explanation: Dict[str, str] = {
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
    def __init__(self, item: Dict[str, Any]) -> None:
        error: Dict[str, Any] = item["error"]
        self.barcode: Optional[str] = item["barcode"]
        self.reference: Optional[str] = item["reference"]
        self.code: str = error["code"]
        self.message: str = errors_explanation[error["code"]]
        self.text: str = error["text"]
        self.input: Optional[str] = error["input"]
        # Field "field" is not mentioned in docs (optional)
        self.field: Optional[str] = error.get("field")

    def __str__(self) -> str:
        return (
            f"ShipmentOrderErrorDetails(barcode={self.barcode}, "
            f"reference={self.reference}, code={self.code}, message={self.message}, "
            f"text={self.text}, input={self.input}, field={self.field})"
        )

    __repr__ = __str__


class ShipmentOrderError(Exception):
    def __init__(self, errors: Dict[str, Any]) -> None:
        self.errors: List[ShipmentOrderErrorDetails] = [
            ShipmentOrderErrorDetails(item) for item in errors["errors"]["item"]
        ]
