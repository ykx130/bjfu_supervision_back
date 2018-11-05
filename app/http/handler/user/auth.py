from app.http.handler.user import user_blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify
from app.core.models.user import User
from app.core.controllers import user_controller
from app.utils.misc import convert_datetime_to_string


@user_blueprint.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
        if username is None or password is None:
            return jsonify({
                "code": 500,
                "message": "username or password can not be null"
            }), 401
        try:
            user = User.query.filter(User.username == username).filter(User.using == True).first()
            if user is None or not user.verify_password(password=password):
                return jsonify({
                    "code": 500,
                    "message": "username or password may be wrong"
                }), 401
            login_user(user, remember=False)
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": str(e)
            }), 500
        return jsonify({
            "code": 200,
            "message": "success"
        }), 200


@user_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500
    return jsonify({
        "code": 200,
        "message": "success"
    }), 200


@user_blueprint.route("/current_user", methods=["GET"])
@login_required
def get_current():
    (user, err) = user_controller.find_user(current_user.username)
    if err is not None:
        return jsonify({
            'code': err.code,
            'message': err.err_info,
            'current_user': None,
        }), err.status_code
    return jsonify({
        'code': 200,
        'message': '',
        'current_user': user
    }), 200
