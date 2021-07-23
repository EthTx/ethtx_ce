from functools import wraps
from typing import Callable

from flask import current_app, Response, request


def check_auth(username: str, password: str) -> bool:
    """This function is called to check if a username /
    password combination is valid.
    """
    return (
        username == current_app.config["ETHTX_ADMIN_USERNAME"]
        and password == current_app.config["ETHTX_ADMIN_PASSWORD"]
    )


def authenticate() -> Response:
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f: Callable):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
