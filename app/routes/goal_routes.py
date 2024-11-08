from flask import Blueprint
from flask import Blueprint, abort, make_response, request
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from .route_utilities import validate_model, create_model, delete_model, get_models_with_query_params

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_query_params(Goal, request.args)

@bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return {"goal": goal.to_dict()}

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    return delete_model(Goal, goal_id)

@bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    request_body["goal_id"] = goal.id
    return create_model(Task, request_body)

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return [task.to_dict() for task in goal.tasks]
