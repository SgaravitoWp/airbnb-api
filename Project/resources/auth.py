from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
from jwt.exceptions import ExpiredSignatureError
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask.views import MethodView
from flask import request, jsonify
from dotenv import load_dotenv
from schemas.schemas import *
from db import db
import models
import os

load_dotenv()

blp = Blueprint("Auth", __name__, description="Operation on Auth")

token_valid_time = int(os.getenv("TOKEN_VALID_TIME"))

@blp.route("/sign-up")
class SignUp(MethodView):

    class_name = "SignUp"

    SuccessResponse = define_response(f"{class_name}SuccessResponse", UserSignUpSchema)
    # BadResponse = define_response("BadResponse", UserSignUpSchema)
    # InternalServerResponse = define_response("InternalServerResponse", UserSignUpSchema)

    @blp.arguments(UserSignUpSchema)
    @blp.response(201, SuccessResponse, description="User Registered")
    # @blp.alt_response(400, BadResponse, description="Bad Request")
    # @blp.alt_response(500, InternalServerResponse, description="Server Error")
    def post(self, data):
        
        username = data.get("username")
        password = data.get("password")

        new_user = User(username=username, password=password)

        try:
            status_code = 201
            db.session.add(new_user)
            db.session.commit()
            return {
                    "success": True, 
                    "message": f"User has been created.",
                    "status_code": status_code,
                    "data": {
                        "user_id": new_user.id
                    }
                    }
        
        except IntegrityError:
            status_code = 400
            db.session.rollback()
            abort(status_code,
                  success = False,
                  message = f"User {data['username']} is already in use",
                  status_code = status_code
                  )

        except Exception:
            status_code = 500
            db.session.rollback()
            abort(status_code,
                  success = False,
                  message = f"Internal server error.",
                  status_code = status_code
                  )

@blp.route("/get-token")
class Authenticate(MethodView):

    class_name = "Authenticate"
    SuccessResponse = define_response(f"{class_name}SuccessResponse", TokenSchema)
    @blp.arguments(UserSchema)
    @blp.response(200, SuccessResponse, description="User Authenticated")
    def post(self, data):
        
        status_code = 401
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "This user is not registered.",
                            "success": False,
                            "status_code": status_code,
                            }), 401
        
        password = check_password_hash(user.password, password)
        if not password: 
            return jsonify({"message": "The submitted password does not match.",
                            "success": False,
                            "status_code": status_code,
                            }), 401
        
        status_code = 200
        token = Token.query.filter_by(user_id=user.id).first()
        if token:
            if token.expiration < datetime.now():
                updated_token = create_access_token(identity={"username":username})
                token.token = updated_token
                token.expiration = datetime.now() + timedelta(hours=token_valid_time)
            else:
                updated_token = token.token
                expiration = token.expiration
        
        else:

            updated_token = create_access_token(identity={"username":username})
            expiration = datetime.now(timezone.utc) + timedelta(hours=token_valid_time)
            new_token = Token(user_id = user.id, token = updated_token, expiration = expiration)
            db.session.add(new_token)

        try:
            status_code = 200
            db.session.commit()
            return {"message": "Bearer Token",
                    "success": True,
                    "data": {"token": updated_token},
                    "status_code": status_code,
                        }
        
        except IntegrityError :
            status_code = 400
            db.session.rollback()
            abort(status_code,
                  success = False,
                  message = f"User {data['username']} is already in use",
                  status_code = status_code
                  )

        except Exception:
            status_code = 500
            db.session.rollback()
            abort(status_code,
                  success = False,
                  message = f"Internal server error.",
                  status_code = status_code
                  )


# @jwt.expired_token_loader
# def token_expirado(jwt_header, jwt_payload):
#     return jsonify({
#         "message": "El token ha expirado.",
#         "error": "token_expired"
#     }), 401
