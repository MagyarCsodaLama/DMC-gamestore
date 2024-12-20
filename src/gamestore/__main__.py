import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from gamestore.game_router import router as gr


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

__version__ = '0.1.0'

def main():
    logger.info('Starting Gamestore %s', __version__)


    app = FastAPI(
        title = 'GameStore',
        version = __version__
    )

    app.include_router(gr)

    @app.get('/')
    def docs():
        return RedirectResponse(url='/docs')

    uvicorn.run(app, log_config=None)



if __name__ == '__main__':
    main()