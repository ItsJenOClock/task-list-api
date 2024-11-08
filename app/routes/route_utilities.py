from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} id {model_id} invalid"}, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    
    except KeyError:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()
    return {f"{cls.__name__.lower()}": new_model.to_dict()}, 201

def delete_model(cls, model_id):
    try:
        model = validate_model(cls, model_id)
    
    except KeyError:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.delete(model)
    db.session.commit()
    return {"details": f"{cls.__name__} {model_id} \"{model.title}\" successfully deleted"}
