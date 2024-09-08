from .base import BaseComponent
from .activity.base import Activity

from selenium.webdriver.remote.webelement import WebElement


class Task(BaseComponent):
    """A Task can have a varying Activity type, but is ultimately a holder for the Rooms (which link to the Activities)."""

    def __init__(self, uuid, element: WebElement, title: str, activity: Activity) -> None:
        super().__init__(element, title)
        self.uuid = uuid
        self.activity = activity