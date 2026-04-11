import logging
import os
import time
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/worker.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

logger.info("Worker started, waiting for tasks...")

while True:
    task = redis_client.brpop("tasks", timeout=5)
    if task:
        logger.info("Worker received task")
        logger.info("Processing task...")
        time.sleep(1)
        logger.info("Task completed")
