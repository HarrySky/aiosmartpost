from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, NotRequired, TypedDict


class SmartPostPlace(TypedDict):
    """Place as returned from new SmartPost API."""

    place_id: str
    name: str
    city: str
    address: str
    country: Literal["EE", "FI", "LV", "LT"]
    postalcode: str
    routingcode: str
    availability: str
    description: str
    type: Literal["apt", "ipb", "po", "pudo"]
    lat: float
    lng: float
    group_id: str
    group_name: str
    group_sort: int
    created_date: str
    updated_date: str


@dataclass(slots=True, frozen=True)
class Place:
    """Place from new SmartPost API as optimized dataclass."""

    place_id: str
    name: str
    city: str
    address: str
    country: Literal["EE", "FI", "LV", "LT"]
    postalcode: str
    routingcode: str
    availability: str
    description: str
    type: Literal["apt", "ipb", "po", "pudo"]
    lat: float
    lng: float
    group_id: str
    group_name: str
    group_sort: int
    created_date: str
    updated_date: str


class OrdersRequestOrders(TypedDict):
    report: list[str]
    # See ShipmentOrder model
    item: list[dict[str, Any]]


class OrdersRequest(TypedDict):
    orders: OrdersRequestOrders


class ShipmentSource(TypedDict):
    country: Literal["ee", "lv", "lt"]


class Sender(TypedDict):
    name: str
    phone: str
    email: NotRequired[str]
    #: Amount of money the sender has to pay before sending the parcel
    cash: NotRequired[float]


class Recipient(TypedDict):
    name: str
    phone: str
    email: NotRequired[str]
    #: Amount of money for goods (goods / transport - only one can be filled)
    goods: NotRequired[float]
    #: Amount of money for transport (goods / transport - only one can be filled)
    transport: NotRequired[float]
    #: ID code of the recipient; needed if ID validation is required.
    idcode: NotRequired[str]


class EETerminalDestination(TypedDict):
    place_id: str
    country: Literal["ee"]


class AddressDestination(TypedDict):
    place_id: Literal["1"]
    postalcode: str
    #: Either just street or street + house + apartment
    street: str
    #: Not required if all info is provided in street
    house: NotRequired[str]
    #: Not required if all info is provided in street
    apartment: NotRequired[str]
    city: str
    country: str
    #: Extra details about the destination (e.g. third floor)
    details: NotRequired[str]
    #: When will the recipient be available for a courier to pick up:
    #: 1 = Any time (default)
    #: 2 = 09:00 – 17:00
    #: 3 = 17:00 – 21:00
    timewindow: Literal[1, 2, 3]


class FIDestination(TypedDict):
    country: Literal["fi"]
    postalcode: str
    routingcode: str


ShipmentDestination = EETerminalDestination | AddressDestination | FIDestination


class AdditionalServices(TypedDict):
    # TODO: DOCUMENT
    labelprinted: NotRequired[bool]


@dataclass(slots=True)
class ShipmentOrder:
    """Shipment order data required to add to order via SmartPost API"""

    #: From where parcel will be sent
    source: ShipmentSource
    recipient: Recipient
    destination: ShipmentDestination
    #: Barcode will be generated if not specified
    barcode: str | None = None
    #: Customer’s reference number (showing on the label)
    reference: str | None = None
    #: Shipment content (showing on the label)
    content: str | None = None
    #: To create multiple parcels with the same data (1-20)
    multiply: int = 1
    #: Weight of the shipment in kg
    weight: float | None = None
    #: Parcel size, required if sent via APT using sender pin code
    size: Literal["XS", "S", "M", "L", "XL"] | None = None
    #: Only needed when "sending with door code" service is used
    sender: Sender | None = None
    #: How many days the customer is able to return order. If customer return is not
    #: allowed, insert 0 (0-90)
    customer_return_days: int | None = None
    #: TODO: Document
    additionalservices: AdditionalServices | None = None

    # TODO: Add return section


class SenderDoorCode(TypedDict):
    doorcode: str


class SmartPostOrder(TypedDict):
    """Just added order as returned from new SmartPost API."""

    barcode: str
    #: Customer’s reference number (showing on the label)
    reference: str
    #: Returned only if sending with door code service is activated
    sender: NotRequired[SenderDoorCode]


@dataclass(slots=True, frozen=True)
class Order:
    """Just added order info from new SmartPost API as optimized dataclass."""

    barcode: str
    reference: str
    sender: SenderDoorCode | None = None
