# Flask Starter Template

A simple flask app starter template with login/register ready. Using Isolated app directory structure.

Here is a list of the available features:

- **Scalable Folder Structure**: The application employs an isolated app directory structure to ensure code
  maintainability and readability.

- **API Ready**: The template includes a ready-to-use API structure, making it suitable for building RESTful services.

- **Web UI**: The template includes a basic web user interface.

- **Rate Limiting**: To protect your application from abuse, rate limiting is enforced.

- **CORS**: Cross-origin resource sharing (CORS) is configured to manage the server's shared resources.

- **Tests**: Unit tests are included to ensure the application's functionality and robustness.

- **Docker Support**: A Dockerfile is included for building a Docker image of your application, facilitating easy
  deployment and scaling.

## Getting Started

### Running The Application

Clone the repository to your local machine:

```bash
git clone https://github.com/riad-azz/flask-template && cd flask-template
```

install the required dependencies:

```bash
pip install -r requirements.txt
```

The application can be run with the following command:

```bash
python server.py
```

### Running Tests

you can write tests in `flask-template/tests`, where you will also find some examples.

To run the tests simply use the command:

```bash
python -m pytest
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

You can check `app/routes/api/examples.py` to get an idea of how the API should work.

### Models

All the models must be dataclasses to be serializable by the `APIResponse`, for example:

```python
from dataclasses import dataclass


@dataclass
class ExampleModel:
    title: str
    content: str
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
        print(error)
        return error_response()
```

If the exception is unknown the API will return a `Internal Server Error` by default from the `error_response()` function.

### API Responses Examples

Run the server and visit the following paths to check the API responses:

- Success Request: [localhost:5000/api/examples/success](http://localhost:5000/api/examples/success)

- Bad Request: [localhost:5000/api/examples/bad-request](http://localhost:5000/api/examples/bad-request)

- Internal Server
  Error: [localhost:5000/api/examples/internal-server-error](http://localhost:5000/api/examples/internal-server-error)

## Contributing

Contributions to improve this Flask app template are welcome. Please feel free to fork the repository, make changes, and
submit a pull request.

## License

This project is licensed under the terms of the MIT license. For more details, see the LICENSE file in the repository.
