from .base import BaseComponent
from .task import Task

from typing import List

from selenium.webdriver.remote.webelement import WebElement


class TaskRow(BaseComponent):
    """Simple row/section for tasks, can be expanded or collapsed through the website."""

    def __init__(self, _id, element: WebElement, title: str, tasks: List[Task] = []) -> None:
        super().__init__(element, title)
        self._id = _id
        self.tasks = tasks

    def _expand(self):
        if (not self.element.get_attribute('aria-expanded')):
            self.element.click()

