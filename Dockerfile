FROM python:3.11.2

# Set the working directory
WORKDIR /code

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]