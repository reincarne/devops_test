import os
import logging
from celery import Celery
from celery.signals import after_setup_logger

log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('worker')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, 'worker.log'))
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

celery_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.addHandler(file_handler)

@celery_app.task(name='worker.process_task')
def process_task():
    logger.info("Worker received task")
    logger.info("Processing task...")
    logger.info("Task completed")
    return "Task completed"
