from typing import List, Literal, Optional

# We don't use it with untrusted random input
from xml.etree.ElementTree import Element, SubElement, tostring  # nosec: B405

from httpx import AsyncClient, Response
from xmltodict import parse as parse_xml  # type: ignore[import]

from smartpost.errors import ShipmentOrderError
from smartpost.models import Destination, OrderInfo, ShipmentOrder


class Client:
    """
    TODO: DOCUMENTATION
    """

    def __init__(self, username: str = "", password: str = "") -> None:  # nosec: B107
        self._client: Optional[AsyncClient] = None
        # Set up authentication XML element
        self._auth = Element("authentication")
        user_el = SubElement(self._auth, "user")
        password_el = SubElement(self._auth, "password")
        user_el.text = username
        password_el.text = password

    @property
    def client(self) -> AsyncClient:
        if not self._client:
            self._client = AsyncClient(
                base_url="https://iseteenindus.smartpost.ee/api",
                http2=True,
            )

        return self._client

    async def get(self, request: str, **kwargs: str) -> Response:
        async with self.client as client:
            return await client.get("/", params={"request": request, **kwargs})

    async def post(self, request: str, xml_content: bytes) -> Response:
        async with self.client as client:
            return await client.post(
                "/", params={"request": request}, content=xml_content
            )

    async def get_ee_terminals(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get("destinations", country="EE", type="APT")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_ee_express_terminals(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get(
            "destinations", country="EE", type="APT", filter="express"
        )
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_fi_terminals(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get("destinations", country="FI", type="APT")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_fi_post_offices(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get("destinations", country="FI", type="PO")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def add_shipment_orders(
        self,
        shipment_orders: List[ShipmentOrder],
        report_emails: Optional[List[str]] = None,
    ) -> List[OrderInfo]:
        """
        TODO: DOCUMENTATION
        """
        document = Element("orders")
        document.insert(0, self._auth)
        report_el = SubElement(document, "report")
        for email in report_emails or []:
            email_el = SubElement(report_el, "email")
            email_el.text = email

        document.extend(order.to_xml() for order in shipment_orders)
        response = await self.post("shipment", tostring(document))
        if response.status_code == 400:
            errors = parse_xml(response.read(), force_list=("item",))
            raise ShipmentOrderError(errors)

        orders = parse_xml(response.read(), force_list=("item",))
        return [OrderInfo(**order) for order in orders["orders"]["item"]]

    async def get_labels_pdf(
        self,
        format: Literal["A5", "A6", "A6-4", "A7", "A7-8"],
        barcodes: List[str],
    ) -> bytes:
        """
        TODO: DOCUMENTATION
        """
        document = Element("labels")
        document.insert(0, self._auth)
        format_el = SubElement(document, "format")
        format_el.text = format
        for barcode in barcodes:
            barcode_el = SubElement(document, "barcode")
            barcode_el.text = barcode

        response = await self.post("labels", tostring(document))
        # TODO: Add request errors handling
        return response.read()
