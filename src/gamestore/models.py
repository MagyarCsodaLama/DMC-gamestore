from pydantic import BaseModel


class CreateGame(BaseModel):
    title: str
    platform: str
    price: float
    release_year: int

class Game(CreateGame):
    id: int


class Order(BaseModel):
    id: int
    customer: str
    status: str
    games: list[Game]