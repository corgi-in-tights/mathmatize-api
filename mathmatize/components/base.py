from selenium.webdriver.remote.webelement import WebElement

class BaseComponent:
    def __init__(self, element: WebElement, title: str) -> None:
        self.element = element
        self.title = title