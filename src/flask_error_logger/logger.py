import os
from pathlib import Path
from typing import Sequence, Union
from flask import Flask
from peewee import IntegrityError

from flask_error_logger.error_logger import ErrorLogger
from flask_error_logger.error_db import create_error_table, ERROR_DB, User, error_db
from flask_error_logger.config import ADMIN_EMAIL, ADMIN_PASSWORD
from flask_error_logger.error_codes import register_handlers


class Logger:
    """
    Initializer class for Logging.

    #### Args:
        * app(Flask): Flask instance
        * error_types(iterable): An optional iterable of HTTP error responses for which logs are to be made. Accepts 4xx and 5xx errors.
            * If 4xx in iterable, all 4xx errors are logged
            * If 5xx in iterable, all 5xx errors are logged
            * example: \n
                [404,"404","4xx","5XX"] # In this case, 4xx will result in logging for all 4xx and 5xx series errors even if they are not specified
        * error_templates(dict|bool): Optional value. 
            * If True, default html templates will be used.
            * If False, json error message will be returned.
            * If a dictionary, only html templates will be used.
                * Templates must be inside a directory in the same level as main app file.
                * If template given for error code, template will be returned.
                * If template not provided for error code, default html templates will be used.
            * example: If dict provided\n
                {
                    "500":"500.html",
                    "404":"404.html"
                }

                If 404 in error_types, "404.html" will be used. Else, default html templates will be used.
        * testing(bool): Whether Logger is being initalised for testing.
        * db_path(str): Path to error db. If None, defaults to path provided in environment. If Path not provided in environment, defaults to one directory above current working directory.

    #### Raises:
        * TypeError: If app is not an instance of Flask
    """

    def __init__(self,
                 app: Flask,
                 error_types: Sequence[str] = ("5xx",),
                 error_templates: Union["dict[str,str]", bool] = None,
                 testing: bool = False,
                 db_path: Path = ERROR_DB):
        self.error_logger = ErrorLogger(app, error_types, error_templates)
        db_instance = self._init_db(Path(db_path))
        self._create_admin(ADMIN_EMAIL, ADMIN_PASSWORD)
        self.error_logger.attach_db(db_instance)

        register_handlers(self.error_logger)

    def _init_db(self, db_path: Path):
        Path.touch(db_path, mode=0o666, exist_ok=True)
        error_db.init(db_path, stale_timeout=300)
        create_error_table()
        return error_db

    def _create_admin(self, email, password):
        try:
            with error_db as db:
                user = User(
                    name="Admin",
                    email=email,
                    role="admin",
                )
                user.set_password(password)
                user.save()
                print("=========user saved")
        except IntegrityError:
            pass
