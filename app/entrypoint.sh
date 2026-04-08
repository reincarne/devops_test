#!/bin/bash
set -e

echo "Starting App Container..."
echo "Running initialization script..."
echo "Application started"

exec gunicorn --bind 0.0.0.0:${APP_PORT:-5000} --workers 2 --threads 2 --worker-class gthread --timeout 30 --access-logfile - app:app


