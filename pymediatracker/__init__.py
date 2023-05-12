"""MediaTracker: Init"""
import logging

from aiohttp import ClientResponse
from typing import List

from .objects.base import MediaTrackerBase
from .objects.config import MediaTrackerConfig
from .objects.item import MediaTrackerItem
from .objects.calendar import MediaTrackerCalendar
from .client import MediaTrackerClient


class MediaTracker(MediaTrackerBase):
    """Interacting with MediaTracker API."""

    logger = logging.getLogger(__name__)

    def __init__(self, client: "MediaTrackerClient", host: str, token: str) -> None:
        """Initialize the appliance."""
        self._client = client
        self._host = host
        self._token = token
        self._config = MediaTrackerConfig
        self._items: List[MediaTrackerItem] = []
        self._calendar: List[MediaTrackerCalendar] = []
        self._entities = [
            {
                "key": "audiobook",
                "name": "Audiobooks",
            },
            {
                "key": "book",
                "name": "Books",
            },
            {
                "key": "movie",
                "name": "Movies",
            },
            {
                "key": "tv",
                "name": "TV Series",
            },
            {
                "key": "video_game",
                "name": "Games",
            },
        ]

    @property
    def host(self) -> str:
        return self._host

    @property
    def token(self) -> str:
        return self._token

    @property
    def items(self) -> List[MediaTrackerItem]:
        return self._items

    @property
    def calendar(self) -> List[MediaTrackerCalendar]:
        return self._calendar

    @property
    def config(self) -> dict:
        return self._config

    @property
    def entities(self) -> dict:
        return self._entities

    async def fetch(self) -> None:
        """Fetch data from MediaTracker."""
        data: dict = {}
        data["config"] = await self.get_config()
        data["items"] = await self.get_items()
        data["entities"] = self.entities
        data["calendar"] = self.calendar

        return data

    async def get_config(self) -> MediaTrackerConfig:
        """Get Config."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/configuration?token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)
        config = [MediaTrackerConfig(self._client, json)]

        return config

    async def get_items(self) -> MediaTrackerItem:
        """Get Items."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/items?token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)

        self._items = [MediaTrackerItem(self._client, item) for item in json or []]
        self._items_dict: dict = {}
        for item in self._items:
            self._items_dict[item.id] = item

    async def get_by_media_type(self, media_type) -> MediaTrackerItem:
        """Get Media."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/items?mediaType={media_type}&token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)

        self._items = [MediaTrackerItem(self._client, item) for item in json or []]
        self._items_dict: dict = {}
        for item in self._items:
            self._items_dict[item.id] = item
