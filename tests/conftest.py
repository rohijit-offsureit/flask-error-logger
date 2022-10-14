import os
from pathlib import Path
import tempfile
import pytest

from flask import Flask

from flask_error_logger import Logger
from flask_error_logger.config import ERROR_DB


# set up base app
@pytest.fixture
def app():
    app = Flask(__name__, instance_relative_config=True)
    db_path = ERROR_DB
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config["ERROR_DB"] = db_path

    @app.get("/")
    def test_get():
        return "Hello"

    @app.get("/get-500")
    def get_500():
        raise ZeroDivisionError

    yield app


# barebones client
@pytest.fixture
def client(app: Flask):
    return app.test_client()


# app implementing rest api
@pytest.fixture
def rest_client(app: Flask):
    Logger(app, error_types=(500, 404), testing=True,
           db_path=app.config['ERROR_DB'])

    @app.get("/body")
    def body():
        return "rest body"
    return app.test_client()


# app inplementing server side rendering with default error code templates
@pytest.fixture
def default_client(app: Flask):
    Logger(app, error_types=(500, 404), error_templates=True, testing=True,
           db_path=app.config['ERROR_DB'])

    @app.get("/body")
    def body():
        return "default body"
    return app.test_client()


# app inplementing server side rendering with custom error code templates
# @pytest.fixture
# def custom_app(app: Flask):
#     Logger(app,error_templates=)


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()
