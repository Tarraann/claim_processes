# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .
RUN chmod +x /app/entrypoint.sh && \
    chmod +x /app/wait-for-it.sh && \
    chmod +x /app/entrypoint_celery.sh && \
    chmod +x /app/entrypoint_celery_scheduler.sh
# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV PYTHONUNBUFFERED=1
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
