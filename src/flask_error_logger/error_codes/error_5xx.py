import traceback
from uuid import uuid4

from flask import Request, render_template
from werkzeug.datastructures import MultiDict

from flask_error_logger.error_db import error_db, ErrorTable
from flask_error_logger.error_templates.default_templates import get_html


# 500
def internal_server_error(request: Request, template: str = None):
    request_data = {
        "user": getattr(request, "user", None),
        "headers": MultiDict(list(request.headers.items())).to_dict(),
        "args": request.args.to_dict(),
        "cookies": request.cookies.to_dict()
    }
    content_type = request.content_type.split(";")[0]
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
            f"error": "Something went wrong.\nError ID:{uid}"
        }, 500
    else:
        if template == "default":
            return get_html(500, uid)
        else:
            return render_template(template, {"error_id": uid})
