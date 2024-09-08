from .base import Activity
from selenium.webdriver.remote.webelement import WebElement

class Poll(Activity):
    def __init__(self, uuid, url, rooms=[]) -> None:
        super().__init__(uuid, url)
        self.rooms = rooms
