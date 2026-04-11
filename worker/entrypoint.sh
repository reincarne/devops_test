#!/bin/bash

echo "Starting Worker Container..."
echo "Running initialization script..."
mkdir -p /var/log/worker

echo "Worker started"
exec python worker.py
