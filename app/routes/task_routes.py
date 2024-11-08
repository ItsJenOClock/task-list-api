from flask import Blueprint, abort, make_response, request
from ..db import db
from app.models.task import Task
from datetime import datetime
import os
import requests
from .route_utilities import validate_model, create_model, delete_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
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

@bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return {"task": task.to_dict()}

@bp.delete("/<task_id>")
def delete_task(task_id):
    return delete_model(Task, task_id)

@bp.patch("/<task_id>/mark_complete")
def update_task_complete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    request_body = {
        "token": os.environ.get("SLACK_BOT_TOKEN"),
        "channel": os.environ.get("SLACK_CHANNEL_ID"), 
        "text": f"Someone just completed the task {task.title}"
    }
    requests.post("https://slack.com/api/chat.postMessage", data=request_body)
    return {"task": task.to_dict()}

@bp.patch("/<task_id>/mark_incomplete")
def update_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}
