from models.tables import *
from schemas.schemas import *
from flask import request, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from app import app, db 


@app.route("/sign-up", methods = ["POST"])
def sign_up():

    data = request.json

    user_schema = UserSchema()
    try:
        data = user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data.get("username")
    password = data.get("password")

    new_user = User(username=username, password=password)
    response = {
        "success": True, 
        "message": f"User {data['username']} has been created.",
        "status_code": 201
    }

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(response), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    