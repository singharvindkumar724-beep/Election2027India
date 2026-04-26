FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default port to 8080 (Cloud Run default)
ENV PORT=8080

# Command to run the application using the PORT env variable
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.backend.main:app
