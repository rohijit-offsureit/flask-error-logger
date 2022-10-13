import os
from flask.testing import FlaskClient


def test_client(client: FlaskClient):
    response = client.get("/")
    assert response.data == b'Hello'


def test_rest_client(rest_client: FlaskClient):
    response = rest_client.get("/body")
    assert response.data == b'rest body'


def test_rest_db(rest_client: FlaskClient):
    db_path = rest_client.application.config['ERROR_DB']
    assert os.path.exists(db_path)


def test_default_client(default_client: FlaskClient):
    response = default_client.get("/body")
    assert response.data == b'default body'


def test_default_db(default_client: FlaskClient):
    db_path = default_client.application.config['ERROR_DB']
    assert os.path.exists(db_path)
