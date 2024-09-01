# Use the official Python image as the base
FROM python:3.12.4-slim

# Set environment variables to prevent Python from writing pyc files and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (if you have any)
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
