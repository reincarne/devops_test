from flask import Flask, jsonify
import redis
import json
import logging
import os
import threading
import signal
import sys

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', '')
worker_port = int(os.getenv('WORKER_PORT', 5001))
log_level = os.getenv('LOG_LEVEL', 'INFO')

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/worker.log'),
        logging.StreamHandler()
    ]
)

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
shutdown_event = threading.Event()

def process_task(task_data):
    logger.info("Worker received task")
    logger.info("Processing task...")
    logger.info(f"Task data: {task_data}")
    logger.info("Task completed")

def listen_for_tasks():
    logger.info("Worker started listening for tasks on Redis")
    while not shutdown_event.is_set():
        try:
            if redis_client:
                task = redis_client.brpop(TASK_QUEUE, timeout=1)
                if task:
                    task_data = json.loads(task[1])
                    process_task(task_data)
        except redis.ConnectionError:
            logger.error("Redis connection lost, retrying...")
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")

def signal_handler(signum, frame):
    logger.info("Shutdown signal received")
    shutdown_event.set()
    sys.exit(0)

@app.route("/")
def home():
    return jsonify({"status": "Worker is running"})

@app.route("/health")
def health():
    try:
        if redis_client:
            redis_client.ping()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy"}), 500

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    task_thread = threading.Thread(target=listen_for_tasks, daemon=True)
    task_thread.start()

    app.run(host="0.0.0.0", port=worker_port, debug=False)
