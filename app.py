from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import socket
from datetime import datetime

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Learn Docker", "done": False},
    {"id": 2, "title": "Deploy with Kubernetes", "done": False},
]
next_id = 3

@app.get("/")
def index():
    return render_template("index.html", tasks=tasks, hostname=socket.gethostname())

@app.get("/health")
def health():
    return jsonify(status="healthy", timestamp=datetime.utcnow().isoformat() + "Z"), 200

@app.get("/api/tasks")
def list_tasks():
    return jsonify(tasks)

@app.post("/api/tasks")
def add_task():
    global next_id
    title = (request.form.get("title") or "").strip()
    if not title:
        return redirect(url_for("index"))
    tasks.append({"id": next_id, "title": title, "done": False})
    next_id += 1
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
