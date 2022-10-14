# Flask Error Logger

A package for logging flask errors and warnings in an sqlite3 db.
#### Note: Custom error handlers cannot be registered while using Logger(for those particular error codes). If custom error handlers are registered(for particular error codes), they will be used instead of Logger.

## Basic Usage
Install using 
`pip install flask-error-logger`

In your code,
```
from flask_error_logger import Logger

app = Flask(__name__)
Logger(app,(404,"429","5xx"),False)

@app.get("/hello")
def hello():
    return "Hello",200
```

## Logger
### Args:

* #### app
  Instance of `Flask`. Required.
* #### error_types
  An optional iterable of HTTP error responses for which logs are to be made. Accepts 4xx and 5xx errors.
  * If 4xx in iterable, all 4xx errors are logged
  * If 5xx in iterable, all 5xx errors are logged
  ##### Example:
    `[404,"429","5xx"]`\
    "5xx" will result in error handlers for all 5xx series HTTP status codes to be registered, even if they are not mentioned in `error_types`
* #### error_templates
  Optional value.
  * If True, default html templates will be used.
  * If False, json error message will be returned.
  * If a dictionary, only html templates will be used.
    * Templates must be inside a directory in the same level as main app file.
    * If template given for error code, template will be returned.
    * If template not provided for error code, default html templates will be used.
    ##### Example
    ```
    {
        "500":"500.html",
        "404":"not_found.html"
    }
    ```
    In the above example, the templates will be used only if they are mentioned in `error_types` argument. Otherwise they will not be registered and you will get `flask`'s default 404 page.
* #### testing
  A boolean value. True, if Logger is being used for testing.
* #### db_path
  A sting or `pathlib.Path` to the database to be used. If None, defaults to path provided in environment. If Path not provided in environment, defaults to one directory above current working directory.

### Raises
* TypeError: If app is not an instance of Flask

## Error Codes Implemented
Although many error types have been implemented, it is recommended to use flask's default error handler since most errors except code:500 do not need to be logged for future review or bug fixes.

* NotFound: 404
* InternalServerError: 500
* NotImplemented: 501
* BadGateway: 502
* ServiceUnavailable: 503
