# Library Management System - Docker Deployment Guide

## Prerequisites

- Docker Desktop installed
- Docker Compose installed (comes with Docker Desktop)

## Quick Start

### 1. Build and Start Containers

```bash
docker-compose up --build
```

This will:
- Build the Django application image
- Pull PostgreSQL 15 image
- Create and start both containers
- Run database migrations automatically
- Start the development server on port 8000

### 2. Access the Application

- **API**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### 3. Create Superuser

In a new terminal, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Docker Commands

### Start Services (Detached Mode)
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (Clean Slate)
```bash
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Run Django Commands
```bash
# Make migrations
docker-compose exec web python manage.py makemigrations

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run tests
docker-compose exec web python manage.py test
```

### Access Django Shell
```bash
docker-compose exec web python manage.py shell
```

### Access PostgreSQL Database
```bash
docker-compose exec db psql -U postgres -d library
```

### Rebuild Containers
```bash
docker-compose up --build
```

## Configuration

### Environment Variables

The `docker-compose.yml` file contains all necessary environment variables:

```yaml
environment:
  - SECRET_KEY=your-secret-key
  - DEBUG=True
  - DB_ENGINE=django.db.backends.postgresql
  - DB_NAME=library
  - DB_USER=postgres
  - DB_PASSWORD=postgres
  - DB_HOST=db
  - DB_PORT=5432
```

**For production**, create a `.env` file and update `docker-compose.yml` to use it:

```yaml
env_file:
  - .env
```

### Volumes

The setup uses three volumes:

1. **postgres_data**: Persists database data
2. **static_volume**: Stores collected static files
3. **media_volume**: Stores uploaded media files

## Project Structure

```
Library Mangement/
├── Dockerfile              # Django app container definition
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore          # Files to exclude from Docker build
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
├── library_app/          # Main Django project
├── user/                 # User app
├── books/                # Books app
└── ...
```

## Services

### Web Service (Django)
- **Container**: library_web
- **Port**: 8000
- **Image**: Built from Dockerfile
- **Depends on**: PostgreSQL database

### Database Service (PostgreSQL)
- **Container**: library_db
- **Port**: 5432
- **Image**: postgres:15-alpine
- **Credentials**:
  - Database: library
  - User: postgres
  - Password: postgres

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use:

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # For web service
  - "5433:5432"  # For database
```

### Database Connection Issues

1. Check if database is healthy:
   ```bash
   docker-compose ps
   ```

2. View database logs:
   ```bash
   docker-compose logs db
   ```

3. Restart services:
   ```bash
   docker-compose restart
   ```

### Permission Issues

On Linux/Mac, you may need to fix permissions:

```bash
sudo chown -R $USER:$USER .
```

### Clean Start

To start fresh with clean database:

```bash
docker-compose down -v
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Production Deployment

For production deployment:

1. **Update settings**:
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Use production server**:
   ```dockerfile
   CMD ["gunicorn", "library_app.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

3. **Add gunicorn to requirements.txt**:
   ```
   gunicorn>=21.2.0
   ```

4. **Use environment variables**:
   - Never commit secrets to git
   - Use `.env` file or container secrets

5. **Set up reverse proxy** (Nginx):
   - Serve static files
   - SSL termination
   - Load balancing

## Health Checks

The PostgreSQL service includes a health check:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

This ensures the web service only starts after the database is ready.

## Backup and Restore

### Backup Database

```bash
docker-compose exec db pg_dump -U postgres library > backup.sql
```

### Restore Database

```bash
docker-compose exec -T db psql -U postgres library < backup.sql
```

## Development Workflow

1. **Start services**:
   ```bash
   docker-compose up
   ```

2. **Make code changes** (hot reload enabled)

3. **Run migrations** if models changed:
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

4. **Run tests**:
   ```bash
   docker-compose exec web python manage.py test
   ```

5. **Stop services** when done:
   ```bash
   docker-compose down
   ```
