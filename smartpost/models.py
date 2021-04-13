from dataclasses import dataclass
from typing import Literal


@dataclass
class Destination:
    place_id: int
    name: str
    city: str
    address: str
    country: Literal["EE", "FI"]
    postalcode: str
    routingcode: str
    availability: str
    description: str
    lat: float
    lng: float

    def __post_init__(self) -> None:
        # All values passed to __init__ are expected to be str
        self.place_id = int(self.place_id)
        self.lat = float(self.lat)
        self.lng = float(self.lng)
