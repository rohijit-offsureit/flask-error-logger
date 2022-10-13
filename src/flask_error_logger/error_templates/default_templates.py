def get_html(error_code, uid=None):
    html = "<!doctype html>\n<html lang=en>"
    if str(error_code) == "500":
        return html + f"""
        <title>500 Internal Server Error</title>
        <h1>Internal Server Error</h1>
        <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
        <p>Error ID: {uid}</p>
        """
    elif str(error_code) == "404":
        return html + f"""
        <html lang=en>
        <title>404 Not Found</title>
        <h1>Not Found</h1>
        <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
        """
