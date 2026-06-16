# Deployment Guide

## Architecture

This project is deployed with Docker Compose and includes three services:

- `db`: PostgreSQL database
- `backend`: FastAPI API service
- `frontend`: Vue static frontend served by Nginx

Main access paths:

- Frontend: `http://127.0.0.1`
- Backend Swagger: `http://127.0.0.1:8000/docs`
- API through Nginx: `http://127.0.0.1/api/articles`

## Environment Variables

Do not commit the real `.env` file. It contains secrets such as the database password and JWT secret key.

Create a local `.env` file from the template.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux / macOS:

```bash
cp .env.example .env
```

For local testing, `.env` can use:

```env
POSTGRES_DB=blog_db
POSTGRES_USER=blog_user
POSTGRES_PASSWORD=blog_password
DATABASE_URL=postgresql://blog_user:blog_password@db:5432/blog_db
SECRET_KEY=dev-secret-key-change-later
FRONTEND_ORIGIN=http://localhost:5173
```

For production deployment:

- Replace `POSTGRES_PASSWORD` with a strong password.
- Replace `SECRET_KEY` with a long random string.
- Replace `FRONTEND_ORIGIN` with the real frontend origin, for example `https://example.com`.

## Local Docker Startup

Start all services:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

Stop services:

```bash
docker compose down
```

Avoid running this unless you intentionally want to delete database data:

```bash
docker compose down -v
```

The `-v` flag removes Docker volumes, including the PostgreSQL data volume.

## Testing

After startup, check:

1. `http://127.0.0.1`
2. `http://127.0.0.1/api/articles`
3. `http://127.0.0.1:8000/docs`

The Docker database starts as a new database. It is normal for articles, categories, and users to be empty at first.

## Database Backup

Create a PostgreSQL backup from the `blog_db` container:

```bash
docker exec blog_db pg_dump -U blog_user blog_db > backup.sql
```

## Database Restore

Linux / macOS:

```bash
cat backup.sql | docker exec -i blog_db psql -U blog_user -d blog_db
```

Windows PowerShell:

```powershell
Get-Content backup.sql | docker exec -i blog_db psql -U blog_user -d blog_db
```

## Uploaded Files and Persistent Data

Uploaded files are stored in the Docker volume:

```text
uploads_data
```

PostgreSQL data is stored in the Docker volume:

```text
postgres_data
```

When migrating to another server, keep:

- Git repository
- `.env`
- Database backup, such as `backup.sql`
- Upload volume data, if uploaded files need to be preserved

## Server Migration Flow

1. Install Docker and Docker Compose.
2. Clone the repository.
3. Create `.env` from `.env.example`.
4. Edit production secrets.
5. Run `docker compose up -d --build`.
6. Restore the database if needed.
7. Point domain DNS to the server IP.
8. Configure HTTPS later.

## Future CI/CD Plan

A later CI/CD setup can use GitHub Actions to:

- Trigger on push to `main`.
- SSH into the server.
- Run `git pull`.
- Run `docker compose up -d --build`.
- Run `docker image prune -f`.

This guide does not include CI/CD configuration files.
