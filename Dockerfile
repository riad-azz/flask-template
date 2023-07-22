# Base image for Python Flask
FROM python:3.11-bullseye

# Python environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /flask-app

# Copy the requirements file
COPY ./requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Flask app file
COPY . .

EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
