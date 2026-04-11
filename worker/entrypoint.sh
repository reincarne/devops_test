#!/bin/bash

echo "Starting Worker Container..."
echo "Running initialization script..."
mkdir -p /app/logs
chown -R 1000:1000 /app/logs

echo "Worker started"
exec su workeruser -s /bin/sh -c "python /app/worker.py"