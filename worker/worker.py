from flask import Flask

app = Flask(__name__)

@app.route("/process")
def process():
    print("Worker received task")
    print("Processing task...")
    return "Task completed"

app.run(host="0.0.0.0", port=5001)