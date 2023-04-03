from typing import Any


class Client:
    """Synchronous SmartPost API client that takes care of all low-level things."""

    def __init__(
        self,
        username: str = "",
        password: str = "",  # nosec: B107
        *,
        read_timeout: int = 10,
    ) -> None:
        raise RuntimeError("Sync client not ported for new API yet")

    @property
    def client(self) -> Any:
        raise NotImplementedError

    def get(self, request: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def post(self, request: Any, xml_content: Any) -> Any:
        raise NotImplementedError

    def get_ee_terminals(self) -> Any:
        raise NotImplementedError

    def get_ee_express_terminals(self) -> Any:
        raise NotImplementedError

    def get_fi_terminals(self) -> Any:
        raise NotImplementedError

    def get_fi_post_offices(self) -> Any:
        raise NotImplementedError

    def add_shipment_orders(
        self,
        shipment_orders: Any,
        report_emails: Any = None,
    ) -> Any:
        raise NotImplementedError

    def get_labels_pdf(
        self,
        format: Any,
        barcodes: Any,
    ) -> Any:
        raise NotImplementedError
