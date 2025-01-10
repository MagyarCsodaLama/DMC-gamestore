import logging

from fastapi.testclient import TestClient
from gamestore.__main__ import app


logger = logging.getLogger(__name__)

def client():

    return TestClient(app)


def test_1():
    c = client()
    g = c.get("/game/1")
    logger.info(g)






