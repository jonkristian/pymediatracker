"""MediaTracker: Base"""
import logging


class MediaTrackerBase:
    """Base class for MediaTracker."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class MediaTrackerBaseClient(MediaTrackerBase):
    """Base class for MediaTracker."""

    def __init__(self, client, attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client
