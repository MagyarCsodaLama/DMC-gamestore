import json
import logging
import uuid

from fastapi.testclient import TestClient
from gamestore.__main__ import app
import pytest


logger = logging.getLogger(__name__)

@pytest.fixture(scope='function')
def test_game():
    return {'title': f'test_game {uuid.uuid4()}', 'platform': 'PC', 'price': 42.42, 'release_year': 2025}

@pytest.fixture(scope='function')
def client():

    return TestClient(app)


def test_create_game(client, test_game):
    r = client.post('/game', content=json.dumps(test_game))

    assert r.status_code == 200

    created_game = r.json()
    logger.debug('Created game: %s', created_game)

    g_id = created_game.get('id')
    assert isinstance(g_id, int)

    created_game_wo_id = {k: v for k, v in created_game.items() if k != 'id'}
    assert created_game_wo_id == test_game


def test_read_game(client, test_game):
    r = client.post('/game', content=json.dumps(test_game))
    created_game = r.json()

    r = client.get(f'/game/{created_game["id"]}')
    assert r.status_code == 200
    read_game = r.json()
    logger.info('Read game: %s', read_game)
    assert read_game == created_game


def test_read_game_sad_case(client):
    r = client.get('/game/-1')
    assert r.status_code == 404
    err_desc = r.json()
    logger.info(err_desc)
    assert err_desc == {'detail': 'Game with id -1 does not exist'}


def test_del_game(client, test_game):
    r = client.post('/game', content=json.dumps(test_game))
    created_game = r.json()

    r = client.get(f'/game/{created_game["id"]}')
    assert r.status_code == 200

    r = client.delete(f'/game/{created_game["id"]}')
    assert r.status_code == 200

    r = client.get(f'/game/{created_game["id"]}')
    assert r.status_code == 404

    deleted_game = r.json()
    logger.info('Deleted game: %s', deleted_game)








