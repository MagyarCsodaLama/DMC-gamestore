from fastapi import APIRouter
from gamestore.models import Game, CreateGame, UpdateGame, Order, FullOrder, CreateOrder, OrderGame
from fastapi import Path
from fastapi import HTTPException, status, Body
from gamestore.db_handler import order_table as db, order_game_table as rel_table, Cursor
from gamestore.game_router import read_game

router = APIRouter(
    tags = ['order']
)

@router.post(
    path='/order',
    response_model=Order
)
def create_order(order:CreateOrder=Body()):
    o = Order(
        **order.model_dump(),
        id=max(db.keys(), default=0) + 1
    )
    db[o.id] = o
    return o

@router.put(
    path='/order/{order_id}/game/{game_id}'
)
def add_game(
        order_id: int = Path(),
        game_id: int = Path()
):
    read_game(game_id)

    game_item = OrderGame(
        id=max(rel_table.keys(), default=0)+1,
        order_id = order_id,
        game_id = game_id
    )

    rel_table[game_item.id] = game_item
    return game_item

@router.get(
    path='/order/{order_id}',
    response_model=FullOrder
)
def read_order(order_id: int = Path()):
    o = db.get(order_id)

    if o is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No order {order_id}')

    with Cursor() as c:
        c.execute("""
                select g.*
                from "order" as o
                inner join order_game as og on og.order_id = o.id
                inner join game as g on og.game_id = g.id
                where o.id = :order_id
            """,
            {'order_id': order_id}
        )
        rows = c.fetchall()

    o = FullOrder.model_validate(o.model_dump())

    for r in rows:
        g = Game(**r)
        o.games.append(g)

    return o




