from pydantic import BaseModel, Field


class CreateGame(BaseModel):
    title: str
    platform: str
    price: float
    release_year: int

class UpdateGame(BaseModel):
    title: str | None = Field(default=None)
    platform: str | None = Field(default=None)
    price: float | None = Field(default=None)
    release_year: int | None = Field(default=None)

class Game(CreateGame):
    id: int






class CreateOrder(BaseModel):
    customer: str
    status: str



class Order(CreateOrder):
    id: int


class FullOrder(Order):
    games: list[Game] = Field(default_factory=lambda: [])


class OrderGame(BaseModel):
    id: int
    order_id: int
    game_id: int