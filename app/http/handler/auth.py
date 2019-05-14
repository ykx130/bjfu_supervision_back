from app.http.handler import user_blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify
import app.core.controller as controller
from app.utils import CustomError


@user_blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    try:
        controller.AuthController.login(username=username, password=password)
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        "code": 200,
        "msg": "success"
    }), 200


@user_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        controller.AuthController.logout()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        "code": 200,
        "msg": "success"
    }), 200


@user_blueprint.route("/current_user", methods=["GET"])
@login_required
def get_current():
    try:
        user = controller.AuthController.get_current_user()
    except CustomError as e:
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'current_user': user
    }), 200
