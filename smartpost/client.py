from typing import List, Optional

# We don't use it with untrusted random input
from xml.etree.ElementTree import Element, SubElement  # nosec: B405

from httpx import AsyncClient, Response
from xmltodict import parse as parse_xml  # type: ignore[import]

from smartpost.models import Destination


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

    async def ee_destinations(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get("destinations", country="EE", type="APT")
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]

    async def ee_express_destinations(self) -> List[Destination]:
        """
        TODO: DOCUMENTATION
        """
        response = await self.get(
            "destinations", country="EE", type="APT", filter="express"
        )
        # TODO: Add request errors handling
        destinations = parse_xml(response.read(), force_list=("item",))
        return [Destination(**item) for item in destinations["destinations"]["item"]]
