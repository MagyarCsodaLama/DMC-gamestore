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


class Order(BaseModel):
    id: int
    customer: str
    status: str
    games: list[Game]