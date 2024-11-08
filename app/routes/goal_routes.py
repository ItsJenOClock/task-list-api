from flask import Blueprint
from flask import Blueprint, abort, make_response, request
from ..db import db
from app.models.goal import Goal
from datetime import datetime
from .route_utilities import validate_model, create_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Goal.title)
    elif sort_param == "desc":
        query = query.order_by(Goal.title.desc())
    else:
        query = query.order_by(Goal.id)

    goals = db.session.scalars(query)
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response, 200

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
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}
