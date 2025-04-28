# Use the official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies if needed (for pip / psycopg2 etc.)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port your Flask app runs on 
EXPOSE 5001

# Set the entrypoint: Gunicorn to serve Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "bff:app"]
