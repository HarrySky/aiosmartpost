from __future__ import annotations

from dataclasses import asdict
from typing import Any, Literal

from httpx import AsyncClient, Response, Timeout

from smartpost.errors import ShipmentLabelsError, ShipmentOrderError
from smartpost.models import (
    Order,
    OrdersRequest,
    Place,
    ShipmentOrder,
    SmartPostOrder,
    SmartPostPlace,
)


class Client:
    """Asynchronous SmartPost API client that takes care of all low-level things."""

    def __init__(
        self,
        api_key: str,
        *,
        read_timeout: int = 10,
    ) -> None:
        self._read_timeout = read_timeout
        self._client: AsyncClient | None = None
        self._api_key = api_key

    @property
    def client(self) -> AsyncClient:
        if not self._client:
            self._client = AsyncClient(
                base_url="https://gateway.posti.fi/smartpost",
                http2=True,
                timeout=Timeout(5, read=self._read_timeout),
                headers={
                    "Authorization": self._api_key,
                    "Content-Type": "application/json",
                },
            )

        return self._client

    async def get(self, endpoint: str, **kwargs: str | list[str]) -> Response:
        return await self.client.get(endpoint, params=kwargs)

    async def post(self, endpoint: str, json_data: dict[str, Any]) -> Response:
        return await self.client.post(endpoint, json=json_data)

    async def get_ee_terminals(self) -> list[Place]:
        """Fetches list of all Estonia terminals.

        Returns:
            A list of `Place` instances representing all Estonia terminals.
        """
        response = await self.get("/api/ext/v1/places", country="EE", type="APT")
        # TODO: Add request errors handling
        data = response.json()
        places: list[SmartPostPlace] = data["places"]["item"]
        return [Place(**place) for place in places]

    async def get_ee_express_terminals(self) -> list[Place]:
        """Fetches list of all Estonia express terminals.

        Returns:
            A list of `Place` instances representing all Estonia express terminals.
        """
        response = await self.get(
            "/api/ext/v1/places", country="EE", type="APT", filter="express"
        )
        # TODO: Add request errors handling
        data = response.json()
        places: list[SmartPostPlace] = data["places"]["item"]
        return [Place(**place) for place in places]

    async def get_fi_terminals(self) -> list[Place]:
        """Fetches list of all Finland terminals.

        Returns:
            A list of `Place` instances representing all Finland terminals.
        """
        response = await self.get("/api/ext/v1/places", country="FI", type="APT")
        # TODO: Add request errors handling
        data = response.json()
        places: list[SmartPostPlace] = data["places"]["item"]
        return [Place(**place) for place in places]

    async def get_fi_post_offices(self) -> list[Place]:
        """Fetches list of all Finland post offices.

        Returns:
            A list of `Place` instances representing all Finland post offices.
        """
        response = await self.get("/api/ext/v1/places", country="FI", type="PO")
        # TODO: Add request errors handling
        data = response.json()
        places: list[SmartPostPlace] = data["places"]["item"]
        return [Place(**place) for place in places]

    async def add_shipment_orders(
        self,
        shipment_orders: list[ShipmentOrder],
        report_emails: list[str] | None = None,
    ) -> list[Order]:
        """Adds shipment orders to SmartPost system.

        Args:
            shipment_orders:
                a list of `ShipmentOrder` instances representing orders to be added.
            report_emails:
                optional list of strings with emails to which
                reports about order will be sent.

        Returns:
            A list of `Order` instances representing all added orders.

        Raises:
            ShipmentOrderError:
                SmartPost API had issues with shipment orders you sent.
        """
        request_data: OrdersRequest = {
            "orders": {
                "report": [],
                "item": [],
            }
        }
        for email in report_emails or []:
            request_data["orders"]["report"].append(email)

        for order in shipment_orders:
            order_dict = {
                key: value for key, value in asdict(order).items() if value is not None
            }
            request_data["orders"]["item"].append(order_dict)

        response = await self.post("/api/ext/v1/orders", dict(request_data))
        if response.status_code == 400:
            errors = response.json()
            raise ShipmentOrderError(errors["error"])

        data = response.json()
        orders: list[SmartPostOrder] = data["orders"]["item"]
        return [Order(**order) for order in orders]

    async def get_labels_pdf(
        self,
        format: Literal["A5", "A6", "A6-4", "A7", "A7-8"],
        barcodes: list[str],
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
        response = await self.get("/api/ext/v1/labels", format=format, barcode=barcodes)
        data = response.read()
        if response.status_code != 200:
            raise ShipmentLabelsError(data, response.status_code)

        return data
