from pydantic import BaseModel

class Game(BaseModel):
    id: int
    title: str
    platform: str
    price: float
    release_year = int


class Order(BaseModel):
    id: int
    customer: str
    status: str
    games: list[Game]