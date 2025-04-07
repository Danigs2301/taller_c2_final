# app.py
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)

tasks = mongo.db.tasks  # Colección de tareas

@app.route('/')
def index():
    all_tasks = list(tasks.find())
    for task in all_tasks:
        task["_id"] = str(task["_id"])
    return render_template('index.html', tasks=all_tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = [{"_id": str(task["_id"]), "title": task["title"], "done": task["done"]} for task in tasks.find()]
    return jsonify(all_tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_id = tasks.insert_one({"title": data["title"], "done": False}).inserted_id
    return jsonify({"message": "Task added", "_id": str(task_id)})

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        return jsonify({"_id": str(task["_id"]), "title": task["title"], "done": task["done"]})
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"title": data["title"], "done": data["done"]}})
    return jsonify({"message": "Task updated"})

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
