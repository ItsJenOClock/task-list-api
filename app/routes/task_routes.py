from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    try:
        request_body = request.get_json()
        title = request_body["title"]
        description = request_body["description"]
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title)
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response, 200

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}

@tasks_bp.patch("/<task_id>/mark_complete")
def update_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task": task.to_dict()}

@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task id {task_id} invalid"}, 400))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task
