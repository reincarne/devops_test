from flask import Flask, jsonify
import redis
import json
import os
import logging

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', '')
app_port = int(os.getenv('APP_PORT', 5000))
log_level = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

try:
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        db=0,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_keepalive=True
    )
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.error(f"Redis connection failed: {str(e)}")
    redis_client = None

TASK_QUEUE = 'task_queue'

@app.route("/")
def home():
    return jsonify({"status": "App is running"})

@app.route("/health")
def health():
    try:
        if redis_client:
            redis_client.ping()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy"}), 500

@app.route("/task", methods=['POST', 'GET'])
def send_task():
    if not redis_client:
        return jsonify({"error": "Redis connection unavailable"}), 503

    try:
        task = {"id": "task_001", "data": "sample_task"}
        redis_client.lpush(TASK_QUEUE, json.dumps(task))
        logger.info(f"Task sent to queue: {task}")
        return jsonify({"message": "Task sent to queue", "task": task}), 200
    except Exception as e:
        logger.error(f"Error sending task: {str(e)}")
        return jsonify({"error": "Error sending task"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_port, debug=False)
