import os
from flask import Flask
import redis

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
APP_PORT = int(os.environ.get("APP_PORT", 5000))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route("/")
def home():
    return "App is running"

@app.route("/health")
def health():
    try:
        redis_client.ping()
        return "OK", 200
    except Exception:
        return "Unhealthy", 500

@app.route("/task")
def send_task():
    try:
        redis_client.lpush("tasks", "new_task")
        return "Task sent to worker via Redis"
    except Exception as e:
        return f"Error sending task: {str(e)}"

app.run(host="0.0.0.0", port=APP_PORT)
