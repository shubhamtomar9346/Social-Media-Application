# Social Networking API

This project is a social networking application built using Django Rest Framework. The API allows users to sign up, log in, search for other users, send and manage friend requests, and list friends. It also enforces rate limiting on the number of friend requests that can be sent within a minute.

## Features

- **User Signup/Login**: Users can sign up with their email and log in with their email and password.
- **Search Users**: Users can search for other users by email or username.
- **Friend Requests**: Users can send, accept, and reject friend requests.
- **List Friends**: Users can view a list of their accepted friends.
- **List Pending Friend Requests**: Users can view a list of received but not yet accepted friend requests.
- **Rate Limiting**: Users cannot send more than 3 friend requests within a minute.

## Technologies Used

- **Python**: 3.12.4
- **Django**: 5.1
- **Django Rest Framework**: 3.15.2
- **SQLite**: Default database
- **Docker**: For containerizing the application

## Installation

### Prerequisites

- **Python 3.12.4**: Ensure Python is installed.
- **Docker**: Install Docker and Docker Compose from [here](https://docs.docker.com/get-docker/).

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd social_network
    ```

2. **(Optional) Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # For Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

### Running with Docker

1. **Build the Docker Image**:
    ```bash
    docker-compose build
    ```

2. **Run the Containers**:
    ```bash
    docker-compose up
    ```

3. **Access the Application**:
    - The application will be available at `http://localhost:8000/`.

4. **Stopping the Application**:
    - Press `Ctrl+C` in the terminal.
    - To remove the containers, run:
        ```bash
        docker-compose down
        ```

## Virtual Environment

This project includes a pre-configured Python virtual environment located in the `magic_box3.12_social_media` folder. 

### Options:

1. **Use Existing Virtual Environment**:
    - You can set `magic_box3.12_social_media` as the interpreter in your IDE (e.g., PyCharm).
  
    - In PyCharm:
        1. Go to `File > Settings > Project: Your Project Name > Python Interpreter`.
        2. Click on the gear icon and select `Add`.
        3. Choose `Existing Environment`.
        4. Navigate to `magic_box3.12_social_media/bin/python` and select it.

2. **Create a New Virtual Environment**:
    - If you prefer, you can create your own virtual environment.
    - Run the following commands:

      ```bash
      python3 -m venv my_new_env
      source my_new_env/bin/activate  # On Windows: my_new_env\Scripts\activate
      pip install -r requirements.txt
      ```

    - Update the interpreter in PyCharm to use the new virtual environment if needed.

## Usage

### API Endpoints

- **User Signup**: `POST /signup/`
- **User Login**: `POST /login/`
- **Search Users**: `GET /search/?q=<search-term>`
- **Send Friend Request**: `POST /friend-request/send/`
- **Accept Friend Request**: `PUT /friend-request/accept/<id>/`
- **Reject Friend Request**: `DELETE /friend-request/reject/<id>/`
- **List Friends**: `GET /friends/`
- **List Pending Friend Requests**: `GET /friend-requests/pending/`

### Testing with Postman

A Postman collection named `Social Media Application.postman_collection.json` is provided in the project folder. Import the collection into Postman to test the API endpoints. The collection includes all the API endpoints with sample requests.

### Rate Limiting

The application enforces a rate limit of 3 friend requests per minute. If a user attempts to send more than 3 friend requests within this period, an error response will be returned.

## Docker Configuration

### Dockerfile

```dockerfile
# Use the official Python image as the base
FROM python:3.12.4-slim

# Set environment variables to prevent Python from writing pyc files and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFEREDIFDEF=1

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

Social Media Application/
│
├── magic_box3.12_social_media/        # Pre-configured Python virtual environment
├── social_network/
│   ├── social_network/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── db.sqlite3
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── manage.py
│   ├── README.md
│   ├── requirements.txt
│   └── Social Media Application.postman_collection.json
└── External Libraries/
