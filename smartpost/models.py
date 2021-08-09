from dataclasses import dataclass, field
from typing import Literal, Optional, TypedDict, Union

# We don't use it with untrusted random input
from xml.etree.ElementTree import Element, SubElement  # nosec: B405


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
        # Values passed to __init__ are expected to be str
        self.place_id = int(self.place_id)
        self.lat = float(self.lat)
        self.lng = float(self.lng)


@dataclass
class Sender:
    name: str
    phone: str
    email: str
    # Amount of money the sender has to pay before sending the parcel
    cash: float
    # Business customer’s account identificator
    account: int


@dataclass
class Recipient:
    name: str
    phone: str
    email: str
    # Amount of money the recipient has to pay before receiving the parcel
    cash: Optional[float] = None
    # ID code of the recipient; needed if ID validation is required.
    idcode: Optional[int] = None

    def to_xml(self) -> Element:
        recipient = Element("recipient")
        name = SubElement(recipient, "name")
        name.text = self.name
        phone = SubElement(recipient, "phone")
        phone.text = self.phone
        email = SubElement(recipient, "email")
        email.text = self.email

        # Optional fields
        if self.cash is not None:
            cash = SubElement(recipient, "cash")
            cash.text = str(self.cash)

        if self.idcode is not None:
            idcode = SubElement(recipient, "idcode")
            idcode.text = str(self.idcode)

        return recipient


@dataclass
class EETerminalDestination:
    place_id: int

    def to_xml(self) -> Element:
        destination = Element("destination")
        place_id = SubElement(destination, "place_id")
        place_id.text = str(self.place_id)
        return destination


@dataclass
class EECourierDestination:
    street: str
    house: str
    apartment: str
    city: str
    country: str
    postalcode: str
    details: str
    timewindow: Literal[1, 2, 3]

    def to_xml(self) -> Element:
        """TODO"""
        return Element("destination")


@dataclass
class FIDestination:
    postalcode: str
    routingcode: str

    def to_xml(self) -> Element:
        destination = Element("destination")
        postalcode = SubElement(destination, "postalcode")
        postalcode.text = self.postalcode
        routingcode = SubElement(destination, "routingcode")
        routingcode.text = self.routingcode
        return destination


ShipmentDestination = Union[EETerminalDestination, EECourierDestination, FIDestination]


@dataclass
class ShipmentOrder:
    recipient: Recipient
    destination: ShipmentDestination
    # Will be generated if not specified
    barcode: Optional[str] = None
    reference: Optional[str] = None
    content: Optional[str] = None
    orderparent: Optional[str] = None
    weight: Optional[float] = None
    size: Optional[Literal[5, 6, 7, 8, 11]] = None
    # Only needed when "sending with door code" service is used
    sender: Optional[Sender] = None
    # TODO: Create proper types
    lqitems: None = None
    additionalservices: None = None

    def to_xml(self) -> Element:
        item = Element("item")
        recipient_el = self.recipient.to_xml()
        item.append(recipient_el)
        destination_el = self.destination.to_xml()
        item.append(destination_el)

        # Optional fields
        if self.barcode:
            barcode = SubElement(item, "barcode")
            barcode.text = self.barcode

        if self.reference:
            reference = SubElement(item, "reference")
            reference.text = self.reference

        if self.content:
            content = SubElement(item, "content")
            content.text = self.content

        if self.orderparent:
            orderparent = SubElement(item, "orderparent")
            orderparent.text = self.orderparent

        if self.weight:
            weight = SubElement(item, "weight")
            weight.text = str(self.weight)

        if self.size:
            size = SubElement(item, "size")
            size.text = str(self.size)

        # TODO: Deal with sender, lqitems and additionalservices

        return item


class SenderDoorCode(TypedDict):
    doorcode: int


@dataclass
class OrderInfo:
    barcode: str
    reference: str
    sender: Optional[SenderDoorCode] = None

    # Convinient access to `sender["doorcode"]`
    doorcode: Optional[int] = field(default=None, init=False)

    def __post_init__(self) -> None:
        if self.sender:
            # Values passed to __init__ are expected to be str
            self.doorcode = int(self.sender["doorcode"])
            self.sender["doorcode"] = self.doorcode
