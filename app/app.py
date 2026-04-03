from flask import Flask
from celery import Celery

app = Flask(__name__)

celery_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.route("/")
def home():
    return "App is running"

@app.route("/task")
def send_task():
    try:
        result = celery_app.send_task('worker.process_task')
        task_result = result.get(timeout=5)
        return f"Worker response: {task_result}"
    except Exception as e:
        return f"Error contacting celery worker: {str(e)}"
