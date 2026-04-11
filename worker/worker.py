import logging
import time
import redis

LOG_DIR = "/var/log/worker"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/worker.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

logger.info("Worker started, waiting for tasks...")

while True:
    task = redis_client.brpop("tasks", timeout=5)
    if task:
        logger.info("Worker received task")
        logger.info("Processing task...")
        time.sleep(1)
        logger.info("Task completed")
