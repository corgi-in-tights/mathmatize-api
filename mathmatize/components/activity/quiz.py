from .base import Activity

class Quiz(Activity):
    def __init__(self, uuid, url) -> None:
        super().__init__(uuid, url)