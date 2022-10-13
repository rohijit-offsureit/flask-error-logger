from flask import render_template

from flask_error_logger.error_templates.default_templates import get_html


# 404
def not_found_error(template: str = None):
    if template is None:
        return {
            f"error": "Something went wrong.\nError ID:{uid}"
        }, 500
    else:
        if template == "default":
            return get_html(404)
        else:
            return render_template(template)
