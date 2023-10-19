# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the docker
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY . /app

# Install the required libraries and tools
RUN pip install flask prophet joblib

# Command to run on container start
CMD [ "python3", "flask_app.py" ]  # assuming you named the Flask script as flask_app.py
