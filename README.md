# Flask Starter Template

A simple Flask app starter template. This is my preference to bootstrap my Flask projects and not a must follow
structure, feel free to change whatever you dislike to fit what you are comfortable with.

## Features

Here is a list of the available features:

- **Scalable Folder Structure**: The application employs an isolated app directory structure to ensure code
  maintainability and readability.

- **API Ready**: The template includes a ready-to-use API structure.

- **Web UI**: The template includes a basic web user interface.

- **User Authentication**: The template integrates Flask-Login for user authentication. It allows users to register, log
  in, and log out. It provides session management, secure password hashing, and user session tracking.

- **Rate Limiting**: To protect your application from abuse, rate limiting is enforced.

- **CORS**: Cross-origin resource sharing (CORS) is configured to manage the server's shared resources.

- **CACHING**: The template includes caching to optimize performance and reduce server load. Caching stores frequently
  requested data temporarily, leading to faster API responses. It enhances user experience and helps handle high traffic
  efficiently.

- **Logging**: The application includes logging capabilities to record relevant events, errors, and messages. Logging
  helps in monitoring and troubleshooting the application during development and production.

- **Tests**: Unit tests are included to ensure the application's functionality and robustness.

- **Docker Support**: A Dockerfile is included for building a Docker image of your application, facilitating easy
  deployment and scaling.

## Getting Started

### Running The Application

1.Clone the repository to your local machine:

```bash
git clone https://github.com/riad-azz/flask-template && cd flask-template
```

2.Install the required dependencies:

```bash
pip install -r requirements.txt
```

3.The application can be run with the following command:

```bash
python server.py
```

4.To enable the Ratelimit and Cache features make sure to copy the `.env.example` content and create a `.env` file:

```.env
# Flask Variables
SECRET_KEY="YOUR-SECRET-KEY"
# Flask Ratelimit
RATELIMIT_ENABLED="True"
RATELIMIT_STORAGE_URI="memory://" # or redis://localhost:6379/0
# Flask Cache
CACHE_ENABLED="True"
CACHE_TYPE="SimpleCache" # or RedisCache
CACHE_STORAGE_URL="YOUR-REDIS-URL" # Required only for CACHE_TYPE RedisCache
```

**Note**: for development you need to create a `.env.dev` file.

### Running Tests

You can write tests in `flask-template/tests`, where you will also find some examples.

To run the tests simply use the command:

```bash
python -m pytest
```

You can switch between running the tests from `.env.dev` _(development environment)_ or `.env` _(production environment)_ by going to `flask-template/tests/__init__.py` and changing the value of `FLASK_DEBUG`:

```python
import os

# Set 'False' to test with .env
# Set 'True' to test with .env.dev
os.environ["FLASK_DEBUG"] = "True"
```

### Dockerize The Application

To run the application in Docker follow these steps:

1.Install [Docker](https://www.docker.com/) on your machine.

2.Build the Docker image for the application:

```bash
docker build -t my-flask-image .
```

3.Run the Docker image:

```bash
docker run -p 5000:5000 --name my-flask-container my-flask-image
```

Open your browser and visit [http://localhost:5000](http://localhost:5000/) to see the website.

## Flask API

This is how I like to set up my API in Flask. You might want to change this with `flask-restful` or whatever library
that suits you.

You can check `app/routes/api/tests.py` to get an idea of how the API should work.

### API Schemas

All the schemas served with the API that are passed to the `success_response` must be **json serializable**. In
this example we use `BaseModel` from [pydantic](https://docs.pydantic.dev/latest/) which allows us to turn the model
into a dict using the `model_dump` function:

```python
from pydantic import BaseModel


class TestModel(BaseModel):
    title: str
    content: str
```

```python
# Flask modules
from flask import Blueprint

# Local modules
from app.schemas.test import TestModel
from app.utils.api import success_response

tests_bp = Blueprint("tests", __name__, url_prefix="/tests")


@tests_bp.route("/success", methods=['GET'])
def test_api_success():
    data = TestModel(title="riad-azz", content="Successful API response")
    data_dict = data.model_dump()
    return success_response(data_dict, 200)
```

### Error handling

For API error handling use `werkzeug.exceptions` exception classes, and if you would like to create custom
exceptions make sure that your exceptions inherit from `HTTPException`.

The API error handler can be found in `app/routes/api/__init__.py`:

```python
# Flask modules
from flask import Blueprint
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded

# Other modules
import logging

# Local modules
from app.utils.api import error_response

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, RateLimitExceeded):
        current_limit = error.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    elif isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        logging.error(error)
        return error_response()
```

If the exception is unknown the API will return a `Internal Server Error` by default from the `error_response`
function.

### API Response Examples

Run the server and visit the following paths to check the API responses:

- Success Request: [localhost:5000/api/tests/success](http://localhost:5000/api/tests/success)

- Rate limited Request _(refresh to get rate
  limited)_: [localhost:5000/api/tests/ratelimit](http://localhost:5000/api/tests/ratelimit)

- Bad Request: [localhost:5000/api/tests/bad-request](http://localhost:5000/api/tests/bad-request)

- Forbidden: [localhost:5000/api/tests/forbidden](http://localhost:5000/api/tests/forbidden)

- Internal Server
  Error: [localhost:5000/api/tests/internal-server-error](http://localhost:5000/api/tests/internal-server-error)

- Unknown
  Exception: [localhost:5000/api/tests/unknown-exception](http://localhost:5000/api/tests/unknown-exception)

## Contributing

Contributions to improve this Flask app template are welcome. Please feel free to fork the repository, make changes, and
submit a pull request.

## License

This project is licensed under the terms of the MIT license. For more details, see the LICENSE file in the repository.
