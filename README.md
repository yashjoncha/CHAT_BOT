# Django ChatBot App with Docker

A basic Django application with Docker configuration for deployment testing.

## Project Structure

```
CHAT_BOT/
├── chatbot_project/       # Django project settings
├── chat/                  # Main Django app
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── entrypoint.sh         # Container startup script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md
```

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and start the containers
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

The application will be available at:
- **Web App**: http://localhost:8000
- **Health Check**: http://localhost:8000/health/
- **Admin Panel**: http://localhost:8000/admin/

### 2. Create a Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Web service only
docker-compose logs -f web
```

### 4. Stop the Application

```bash
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Key variables:
- `SECRET_KEY`: Django secret key (change in production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_*`: Database configuration

## API Endpoints

- `GET /` - Home endpoint (returns JSON with app info)
- `GET /health/` - Health check endpoint
- `GET /admin/` - Django admin panel

## Development

### Local Development (without Docker)

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Run development server:
```bash
python manage.py runserver
```

## Services

### Web Service (Django + Gunicorn)
- Python 3.11
- Django 5.0.1
- Gunicorn WSGI server
- WhiteNoise for static files

### Database Service
- PostgreSQL 15
- Persistent volume storage

## Deployment Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Update `ALLOWED_HOSTS` with your domain
- Use environment-specific database credentials
- Configure proper CORS settings if needed
- Set up proper logging

## Technologies Used

- **Django 5.0.1** - Web framework
- **PostgreSQL 15** - Database
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **Docker & Docker Compose** - Containerization
