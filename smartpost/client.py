from typing import List, Literal, Optional

# We don't use it with untrusted random input
from xml.etree.ElementTree import Element, SubElement, tostring  # nosec: B405

from httpx import AsyncClient, Response, Timeout
from xmltodict import parse as parse_xml  # type: ignore[import]

from smartpost.errors import ShipmentOrderError
from smartpost.models import Destination, OrderInfo, ShipmentOrder


class Client:
    """Asynchronous SmartPost API client that takes care of all low-level things."""

    def __init__(
        self,
        username: str = "",
        password: str = "",  # nosec: B107
        *,
        read_timeout: int = 10,
    ) -> None:
        self._read_timeout = read_timeout
        self._client: Optional[AsyncClient] = None

        # XML element "authentication" will be sent with requests that require auth

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
                timeout=Timeout(5, read=self._read_timeout),
            )

        return self._client

    async def get(self, request: str, **kwargs: str) -> Response:
        return await self.client.get("/", params={"request": request, **kwargs})

    async def post(self, request: str, xml_content: bytes) -> Response:
        return await self.client.post(
            "/", params={"request": request}, content=xml_content
        )

    async def get_ee_terminals(self) -> List[Destination]:
        """Fetches list of all Estonia terminals.

        Returns:
            A list of `Destination` instances representing all Estonia terminals.
        """
        response = await self.get("destinations", country="EE", type="APT")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_ee_express_terminals(self) -> List[Destination]:
        """Fetches list of all Estonia express terminals.

        Returns:
            A list of `Destination` instances
            representing all Estonia express terminals.
        """
        response = await self.get(
            "destinations", country="EE", type="APT", filter="express"
        )
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_fi_terminals(self) -> List[Destination]:
        """Fetches list of all Finland terminals.

        Returns:
            A list of `Destination` instances representing all Finland terminals.
        """
        response = await self.get("destinations", country="FI", type="APT")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def get_fi_post_offices(self) -> List[Destination]:
        """Fetches list of all Finland post offices.

        Returns:
            A list of `Destination` instances representing all Finland post offices.
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
        """Adds shipment orders to SmartPost system.

        Args:
            shipment_orders:
                a list of `ShipmentOrder` instances representing orders to be added.
            report_emails:
                optional list of strings with emails to which
                reports about order will be sent.

        Returns:
            A list of `OrderInfo` instances representing all added orders.

        Raises:
            ShipmentOrderError:
                SmartPost API had issues with shipment orders you sent.
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
        """Requests PDF file with labels for orders.

        Args:
            format:
                a string with PDF page format, any of the following:
                A5, A6, A6-4, A7, A7-8.
            barcodes:
                a list of strings with order barcodes for which labels are requested.

        Returns:
            A PDF file bytes. File will contain a page for each barcode provided in
            `barcodes` argument, all pages will be in format from `format` argument.

        Raises:
            httpx.ReadTimeout:
                SmartPost API did not manage to send PDF file in time.
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
