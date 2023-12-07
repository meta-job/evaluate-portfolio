import uuid
from ...database.MySQL import MySQL
from pydantic import Basemodel


class Portfolio(Basemodel):
    def __init__(self) -> None:
        self.user_id = ""