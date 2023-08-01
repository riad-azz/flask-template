# Flask modules
from flask import request, make_response
from flask_limiter import Limiter, RequestLimit
from flask_limiter.util import get_remote_address


def default_exempt_when():
    # You can whitelist IPs from the rate limiter here
    # or put whatever cases you would like the limiter
    # to not work or be ignored
    EXEMPTED_HOSTS = ["127.0.0.1", "localhost"]
    return request.remote_addr in EXEMPTED_HOSTS


def default_error_responder(request_limit: RequestLimit):
    response = """
    <title>429 Too Many Requests</title>
    <h1>Too Many Requests</h1>
    <p>We kindly request your cooperation in refraining from engaging in an unusually high volume of requests.</p>
    """
    return make_response(response, 429)


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['30/minute'],
    on_breach=default_error_responder,
    # default_limits_exempt_when=default_exempt_when,
)
