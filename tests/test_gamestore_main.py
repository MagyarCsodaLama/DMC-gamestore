import logging

from gamestore.__main__ import main

logger = logging.getLogger(__name__)


def log_instead_of_run(*a, **kwa):
    logger.info('I would run: %s, %s', a, kwa)

def test_main(mocker):
    mocker.patch('uvicorn.run', log_instead_of_run)
    main()
