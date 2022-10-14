from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    RequestTimeout,
    Conflict,
    Gone,
    LengthRequired,
    PreconditionFailed,
    RequestEntityTooLarge,
    RequestURITooLarge,
    UnsupportedMediaType,
    RequestedRangeNotSatisfiable,
    ExpectationFailed,
    UnprocessableEntity,
    Locked,
    FailedDependency,
    PreconditionRequired,
    TooManyRequests,
    RequestHeaderFieldsTooLarge,
    UnavailableForLegalReasons,
    # 5xx
    InternalServerError,
    NotImplemented,
    BadGateway,
    ServiceUnavailable,
    GatewayTimeout,
    HTTPVersionNotSupported
)
from flask import request


from flask_error_logger.error_logger import ErrorLogger
from flask_error_logger.error_codes.error_5xx import (
    internal_server_error
)
from flask_error_logger.error_codes.error_4xx import (
    not_found_error
)


def register_handlers(error_logger: ErrorLogger):
    @error_logger.app.errorhandler(Exception)  # 500
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        else:
            template_name = None if not error_logger.show_templates else error_logger.error_templates.get(
                "500", "default")
            return internal_server_error(e, request, template_name, error_db=error_logger.db)

    if error_logger.all_4xx or "404" in error_logger.error_types:  # 404
        @error_logger.app.errorhandler(NotFound)
        def main_404_fn(e):
            template_name = None if not error_logger.show_templates else error_logger.error_templates.get(
                "404", "default")
            return not_found_error(e, template_name)

    if error_logger.all_5xx or "500" in error_logger.error_types:
        @error_logger.app.errorhandler(InternalServerError)  # 500
        def main_500_fn(e: InternalServerError):
            template_name = None if not error_logger.show_templates else error_logger.error_templates.get(
                "500", "default")
            return internal_server_error(e, request, template_name, error_db=error_logger.db)
