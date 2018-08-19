from app.http.handler.user import user_blueprint
from flask_login import current_user,login_user, logout_user,login_required
from flask import request, jsonify
from app.core.models.user import User
from app.utils.misc import convert_datetime_to_string


@user_blueprint.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
        if username is None or password is None:
            return jsonify({
                "code":500,
                "message":"username or password can not be null"
            })
        try:
            user = User.query.filter(User.username == username).first()
            if user is None or not user.verify_password(password=password):
                return jsonify({
                    "code":500,
                    "message":"username or password may be wrong"
                })

            login_user(user, remember=False)
        except Exception as e:
            return jsonify({
                "code":200,
                "message":str(e)
            })
        return jsonify({
            "code":200,
            "message":"success"
        })


@user_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        return jsonify({
            "code":500,
            "message":str(e)
        })
    return jsonify({
        "code":200,
        "message":"success"
    })

@user_blueprint.route("/current_user",methods=["GET"])
def get_current():
    try:
        user = User.query.filter(User.username == current_user.username).first()
    except Exception as e:
        return jsonify({
            "code":500,
            "message":str(e)
        })
    return jsonify({
        "code":200,
        "message":"",
        "user":{
            'id':user.id,
            'username':user.username,
            'name':user.name,
            'start_time':convert_datetime_to_string(user.start_time),
            'end_time':convert_datetime_to_string(user.end_time),
            'sex':user.sex,
            'email':user.email,
            'phone':user.phone,
            'state':user.state,
            'unit':user.unit,
            'status':user.status,
            'work_state':user.work_state,
            'prorank':user.prorank,
            'skill':user.skill,
            'group':user.group,
            'role_names':[role.name for role in user.roles]
        }
    })

