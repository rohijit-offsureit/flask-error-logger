from flask import render_template
from werkzeug.exceptions import (
    NotFound
)


from flask_error_logger.error_templates.default_templates import get_html


# 404
def not_found_error(e: NotFound, template: str = None):
    if template is None:
        return {
            f"error": "URL Not Found",
        }, 404
    else:
        if template == "default":
            return e.get_body()
        else:
            return render_template(template)
