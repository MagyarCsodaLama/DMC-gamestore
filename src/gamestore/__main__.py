import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from gamestore.game_router import router as gr
from gamestore.order_router import router as o_r


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

__version__ = '0.1.0'

app = FastAPI(
    title='GameStore',
    version=__version__
)


app.include_router(gr)
app.include_router(o_r)
@app.get('/')
def docs():
    return RedirectResponse(url='/docs')


def main():
    logger.info('Starting Gamestore %s', __version__)

    uvicorn.run(app, log_config=None)



if __name__ == '__main__':
    main()