import os
import traceback
from uuid import uuid4

from flask import Request, render_template
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import (
    InternalServerError
)
from playhouse.pool import PooledSqliteDatabase

from flask_error_logger.error_db import error_db, ErrorTable
from flask_error_logger.error_templates.default_templates import get_html


class NoDBError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


# 500
def internal_server_error(e: InternalServerError, request: Request, template: str = None, error_db: PooledSqliteDatabase = None):
    if error_db is None:
        raise NoDBError("error_db is required")
    request_data = {
        "user": getattr(request, "user", None),
        "headers": MultiDict(list(request.headers.items())).to_dict(),
        "args": request.args.to_dict(),
        "cookies": request.cookies.to_dict()
    }
    request_content_type = request.content_type
    request_data = {}
    if request_content_type is not None:
        content_type = request_content_type.split(";")[0]
        if content_type == "application/json":
            request_data['body'] = request.json
        elif content_type == "multipart/form-data":
            request_data['body'] = request.form.to_dict()
    uid = str(uuid4()).split("-")[-1]
    with error_db as db:
        ErrorTable.create(
            uid=uid,
            url=request.url,
            method=request.method,
            context=request_data,
            error_trace=traceback.format_exc(),
        )
    if template is None:
        return {
            "error": f"Something went wrong.\nError ID:{uid}"
        }, 500
    else:
        if template == "default":
            return e.get_body() + f"<p>Error ID: {uid}</p>", 500
        else:
            return render_template(template, {"error_id": uid}), 500
