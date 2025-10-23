# Docker Setup for Personal Website

This document provides instructions for running the Flask personal website using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the website:**
   Open your browser and go to `http://localhost:5000`

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the Docker image:**
   ```bash
   docker build -t personal-website .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/projects.db:/app/projects.db personal-website
   ```

3. **Access the website:**
   Open your browser and go to `http://localhost:5000`

## Docker Configuration

### Dockerfile Features

- **Base Image:** Python 3.11 slim for optimal size
- **Security:** Non-root user execution
- **Health Check:** Built-in health monitoring
- **Optimization:** Multi-stage build with dependency caching

### Docker Compose Features

- **Volume Mounting:** Database persistence
- **Health Checks:** Automatic container monitoring
- **Restart Policy:** Automatic restart on failure
- **Environment Variables:** Production-ready configuration

## File Structure

```
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore          # Files to exclude from build
├── DOCKER.md              # This documentation
└── requirements.txt        # Python dependencies
```

## Environment Variables

The following environment variables are set in the Dockerfile:

- `PYTHONDONTWRITEBYTECODE=1` - Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED=1` - Ensures Python output is sent straight to terminal
- `FLASK_APP=app.py` - Specifies the Flask application entry point
- `FLASK_ENV=production` - Sets Flask to production mode

## Volume Mounts

### Database Persistence
```yaml
volumes:
  - ./projects.db:/app/projects.db
```
This ensures your project data persists between container restarts.

### Development Mode (Optional)
```yaml
volumes:
  - ./static:/app/static
```
Mount static files for live development updates.

## Health Checks

The container includes health checks that:
- Check every 30 seconds
- Timeout after 10 seconds
- Retry up to 3 times
- Wait 40 seconds before starting checks

## Production Deployment

### Using Docker Compose

1. **For production deployment:**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Using Docker Swarm or Kubernetes

The application is containerized and ready for orchestration platforms:
- Docker Swarm
- Kubernetes
- AWS ECS
- Google Cloud Run
- Azure Container Instances

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8080:5000"  # Use port 8080 instead
   ```

2. **Database not persisting:**
   ```bash
   # Ensure volume mount is correct
   docker-compose down
   docker-compose up --build
   ```

3. **Permission issues:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Debugging

1. **View container logs:**
   ```bash
   docker-compose logs web
   ```

2. **Access container shell:**
   ```bash
   docker-compose exec web bash
   ```

3. **Check container health:**
   ```bash
   docker-compose ps
   ```

## Security Considerations

- Container runs as non-root user
- Minimal base image (Python slim)
- No unnecessary packages installed
- Health checks for monitoring
- Environment variables for configuration

## Performance Optimization

- Multi-layer caching for faster builds
- Minimal image size with slim base
- Efficient dependency installation
- Health check monitoring
- Restart policies for reliability

## Testing in Docker

### Running Tests in Container

1. **Run tests in the container:**
   ```bash
   docker-compose exec web python -m pytest -v
   ```

2. **Run tests with coverage:**
   ```bash
   docker-compose exec web python -m pytest --cov=app --cov=DAL --cov-report=term-missing
   ```

3. **Run specific test files:**
   ```bash
   docker-compose exec web python -m pytest test_database.py -v
   docker-compose exec web python -m pytest test_app.py -v
   ```

## Development Workflow

1. **Make changes to your code**
2. **Rebuild the container:**
   ```bash
   docker-compose up --build
   ```
3. **Test your changes**
4. **Commit your changes**

## Backup and Restore

### Backup Database
```bash
# Copy the database file
cp projects.db projects.db.backup
```

### Restore Database
```bash
# Restore from backup
cp projects.db.backup projects.db
docker-compose restart
```

## Monitoring

The application includes:
- Health check endpoints
- Container restart policies
- Log aggregation capabilities
- Resource monitoring

## Next Steps

- Set up reverse proxy (nginx) for production
- Configure SSL certificates
- Set up monitoring and logging
- Implement CI/CD pipeline
- Deploy to cloud platform

---

For more information about Docker, visit the [official Docker documentation](https://docs.docker.com/).
