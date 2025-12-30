# Docker Deployment Guide

## Prerequisites
- Docker Engine installed
- Docker Compose installed

## Quick Start

### 1. Set up environment variables

Copy the example .env file and update values:
```bash
cp .env.example .env
```

Update the `.env` file with:
```
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Build and run with Docker Compose

```bash
docker compose -f local.yml up --build
```

Or run in detached mode:
```bash
docker compose -f local.yml up -d --build
```

### 3. Access the application

Open your browser and go to http://localhost:8000

**Default superuser credentials** (created automatically):
- Username: `admin`
- Password: `admin123`

## What Happens Automatically

When you run `docker compose up`, the entrypoint script automatically:

1. ✅ **Runs database migrations** (`python manage.py migrate`)
2. ✅ **Collects static files** with whitenoise (`python manage.py collectstatic`)
3. ✅ **Creates a superuser** (if one doesn't exist) with username `admin` and password `admin123`
4. ✅ **Starts the development server** on port 8000

## Docker Commands

### View logs
```bash
docker compose -f local.yml logs -f
```

### Stop containers
```bash
docker compose -f local.yml down
```

### Stop and remove volumes (⚠️ deletes database)
```bash
docker compose -f local.yml down -v
```

### Rebuild containers
```bash
docker compose -f local.yml up --build
```

### Access Django shell
```bash
docker compose -f local.yml exec web python manage.py shell
```

### Create migrations
```bash
docker compose -f local.yml exec web python manage.py makemigrations
```

### Run custom management commands
```bash
docker compose -f local.yml exec web python manage.py <command>
```

## Services

### Web Service
- Container: `swifttrack_web`
- Port: `8000`
- Framework: Django 5.x
- Database: SQLite3
- Static files: Served via WhiteNoise

## Volumes

- `db_volume`: SQLite database file
- `static_volume`: Collected static files
- `media_volume`: User uploaded media files

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |

## Troubleshooting

### Port already in use
If port 8000 is already in use, change it in `local.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database connection errors
Make sure the database service is running:
```bash
docker compose -f local.yml ps
```

### Static files not loading
Run collectstatic manually:
```bash
docker compose -f local.yml exec web python manage.py collectstatic --noinput
```

### Reset everything
```bash
docker compose -f local.yml down -v
docker compose -f local.yml up --build
```

## Production Notes

For production deployment:
1. Set `DEBUG=False` in your .env
2. Update `ALLOWED_HOSTS` with your domain
3. Generate a strong `SECRET_KEY`
4. Use strong database credentials
5. Consider using Gunicorn instead of runserver
6. Set up proper SSL/TLS certificates
7. Use a reverse proxy like Nginx

---

**Happy Coding! 🚀**
