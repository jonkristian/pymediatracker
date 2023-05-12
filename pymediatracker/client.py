"""MediaTracker: Api"""
import logging
from asyncio import get_event_loop
import async_timeout

from aiohttp import ClientSession, ClientResponse

from .exceptions import MediaTrackerException


class MediaTrackerClient:
    """Connection to MediaTracker API."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize."""
        self._session = session

    async def get(self, url: str, **kwargs) -> ClientResponse:
        """Make a GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> ClientResponse:
        """Make a POST request."""
        return await self.request("POST", url, **kwargs)

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["Content-Type"] = "application/json"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            response: ClientResponse = await self._session.request(
                method,
                url,
                headers=headers,
                **kwargs,
            )
        if response.status != 200:
            raise MediaTrackerException(
                {
                    "request": {
                        "method": method,
                        "url": url,
                        "headers": headers,
                        **kwargs,
                    },
                    "response": await response.json(),
                    "status": response.status,
                }
            )
        return response
