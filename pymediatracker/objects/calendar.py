"""
Class object for MediaTrackerCalendar
Documentation:

Generated by generator/generator.py - 2023-05-10 20:22:42.735267
"""
from .base import MediaTrackerBase, MediaTrackerBaseClient


class Mediaitem(MediaTrackerBase):
    @property
    def id(self):
        return self.attributes.get("id", None)

    @property
    def title(self):
        return self.attributes.get("title", "")

    @property
    def releaseDate(self):
        return self.attributes.get("releaseDate", "")

    @property
    def slug(self):
        return self.attributes.get("slug", "")

    @property
    def mediaType(self):
        return self.attributes.get("mediaType", "")

    @property
    def seen(self):
        return self.attributes.get("seen", True)


class Episode(MediaTrackerBase):
    @property
    def id(self):
        return self.attributes.get("id", None)

    @property
    def title(self):
        return self.attributes.get("title", "")

    @property
    def episodeNumber(self):
        return self.attributes.get("episodeNumber", None)

    @property
    def seasonNumber(self):
        return self.attributes.get("seasonNumber", None)

    @property
    def releaseDate(self):
        return self.attributes.get("releaseDate", "")

    @property
    def isSpecialEpisode(self):
        return self.attributes.get("isSpecialEpisode", True)

    @property
    def seen(self):
        return self.attributes.get("seen", True)


class MediaTrackerCalendar(MediaTrackerBaseClient):
    @property
    def releaseDate(self):
        return self.attributes.get("releaseDate", "")

    @property
    def mediaItem(self):
        return Mediaitem(self.attributes.get("mediaItem", {}))

    @property
    def episode(self):
        return Episode(self.attributes.get("episode", {}))