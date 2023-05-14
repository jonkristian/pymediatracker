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
        self._item: List[MediaTrackerItem] = []
        self._item_dict: dict = {}
        self._calendar_items: List[MediaTrackerCalendar] = []
        self._calendar_items_dict: dict = {}

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
    def item(self) -> List[MediaTrackerItem]:
        return self._item

    @property
    def calendar_items(self) -> List[MediaTrackerCalendar]:
        return self._calendar_items

    @property
    def calendar_items_dict(self) -> dict:
        return self._calendar_items_dict

    @property
    def config(self) -> dict:
        return self._config

    @property
    def entities(self) -> dict:
        return self._entities

    async def fetch(self) -> None:
        """Fetch some basic data from MediaTracker."""
        data: dict = {}
        data["config"] = await self.get_config()
        data["entities"] = self.entities

        return data

    async def get_config(self) -> MediaTrackerConfig:
        """Get MediaTracker Configuration."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/configuration?token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)
        config = [MediaTrackerConfig(self._client, json)]

        return config


    async def get_calendar_items(self, start, end) -> MediaTrackerCalendar:
        """Get MediaTracker Calendar Items from Date Range."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/calendar?start={start}&end={end}&token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)

        self._calendar_items = [
            MediaTrackerCalendar(self._client, calendar_item) for calendar_item in json or []
        ]

        return self._calendar_items


    async def get_item(self, id) -> MediaTrackerItem:
        """Get Item."""
        response: ClientResponse = await self._client.get(
            f"http://{self._host}/api/details/{id}?token={self._token}"
        )
        json = await response.json()
        self.logger.debug(json)

        self._item = MediaTrackerItem(self._client, json)

        return self._item