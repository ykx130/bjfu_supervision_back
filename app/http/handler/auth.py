from app.http.handler import user_blueprint, captcha_bp
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify, Blueprint
import app.core.controller as controller
import app.core.services as service
from app.utils import CustomError, db

@user_blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    try:
        controller.AuthController.login(username=username, password=password)
    except CustomError as e:
        db.session.rollback()
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
        db.session.rollback()
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
        db.session.rollback()
        return jsonify({
            'code': e.code,
            'msg': e.err_info,
        }), e.status_code
    return jsonify({
        'code': 200,
        'msg': '',
        'current_user': user
    }), 200


@user_blueprint.route("/401", methods=["GET"])
def error_401():
    return jsonify({
        'code': 401,
        'msg': '',
    }), 401


@captcha_bp.route('/captcha', methods=['GET'])
def get_captcha():
    try:
        (id, path) = controller.CaptchaController.new_captcha()
    except Exception as e:
        return jsonify(code=500, msg=str(e)), 500
    return jsonify(code=200, uuid=id, path=path)
