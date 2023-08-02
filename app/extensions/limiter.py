# Flask modules
from flask import make_response
from flask_limiter import Limiter, RequestLimit
from flask_limiter.util import get_remote_address


def default_error_responder(request_limit: RequestLimit):
    response = """
    <title>429 Too Many Requests</title>
    <h1>Too Many Requests</h1>
    <p>We kindly request your cooperation in refraining from engaging in an unusually high volume of requests.</p>
    """
    return make_response(response, 429)


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/minute"],
    auto_check=False,
    on_breach=default_error_responder,
)
