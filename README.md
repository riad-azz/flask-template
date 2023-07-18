# Flask Starter Template

A simple flask app starter template with login/register ready. Using Isolated app directory structure.

## Getting Started

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

**Testing**: you can write tests in `flask-template/tests`, and to run the tests simple use the command:

```bash
python -m pytest
```

**Docker**: To run the application in Docker follow these steps:

1.Install [Docker](https://www.docker.com/) on your machine.

2.Build the Docker image for the application:

```bash
docker build -t flask-app .
```

3.Run the Docker image:

```bash
docker run -p 5000:5000 flask-app
```

## Features

- **Scalable Folder Structure**: The application employs an isolated app directory structure to ensure code maintainability and readability.

- **API Ready**: The template includes a ready-to-use API structure, making it suitable for building RESTful services.

- **Web UI**: The template includes a basic web user interface.

- **Rate Limiting**: To protect your application from abuse, rate limiting is enforced.

- **CORS**: Cross-origin resource sharing (CORS) is configured to manage the server's shared resources.

- **Tests**: Unit tests are included to ensure the application's functionality and robustness.

- **Docker Support**: A Dockerfile is included for building a Docker image of your application, facilitating easy deployment and scaling.

## Contributing

Contributions to improve this Flask app template are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the terms of the MIT license. For more details, see the LICENSE file in the repository.
