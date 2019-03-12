from app.core.models.activity import Activity, ActivityUser
from app.core.services import user_service
from app.core.models.lesson import Term
from app.core.models.user import User
from flask_login import current_user
from sqlalchemy.sql import or_
from datetime import datetime
from app.utils.mysql import db
from app.utils.Error import CustomError


def activity_user_dict(id, user):
    (user_model, err) = user_service.user_to_dict(user)
    if err is not None:
        return None, err
    try:
        act_user_dict = {
            "user": user_model,
            "state": ActivityUser.activity_user_state(id, user.username).state,
            "fin_state": ActivityUser.activity_user_state(id, user.username).fin_state
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return act_user_dict, None


def find_activity_users(id, condition):
    try:
        activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    try:
        users = activity.activity_users
    except Exception as e:
        return None, None, CustomError(500, 500, str(e))
    page = int(condition['_page'][0]) if '_page' in condition else 1
    per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_activity_user(id, username):
    try:
        activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    try:
        user = activity.activity_users.filter(User.username == username).first()
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    if user is None:
        return None, CustomError(404, 404, 'user not found')
    return user, None


def insert_activity_user(id, request_json):
    username = request_json.get('username', current_user.username)
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, CustomError(404, 404, "user not found")
    activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    if activity is None:
        return False, CustomError(404, 404, "activity not found")
    if activity.apply_state in ["报名未开始", "报名已结束"]:
        return False, CustomError(500, 200, activity.state)
    if activity.remainder_num <= 0:
        return False, CustomError(500, 200, "remain number is zero")
    activity_user = ActivityUser()
    activity_user.username = user.username
    for key, value in request_json.items():
        if key in ['state', 'user']:
            continue
        if hasattr(activity_user, key):
            setattr(activity_user, key, value)
    activity_user.activity_id = id
    activity_user.state = '已报名'
    activity.remainder_num = activity.remainder_num - 1
    activity.attend_num = activity.attend_num + 1
    db.session.add(activity_user)
    db.session.add(activity)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def update_activity_user(id, username, request_json):
    if username is None:
        return False, CustomError(500, 200, "username should be given")
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, CustomError(404, 404, "user not found")
    activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
    if activity is None:
        return False, CustomError(404, 404, "activity not found")
    activity_user = ActivityUser.query.filter(Activity.id == id).filter(User.username == username).filter(
        ActivityUser.using == True).first()
    if activity_user is None:
        return False, CustomError(404, 404, "user does not attend this activity")
    for key, value in request_json.items():
        if key in ['state', 'user']:
            continue
        if hasattr(activity_user, key):
            setattr(activity_user, key, value)
    db.session.add(activity_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def delete_activity_user(id, username):
    if username is None:
        return False, CustomError(500, 200, "username should be given")
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, CustomError(404, 404, "user not found")
    activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
    if activity is None:
        return False, CustomError(404, 404, "activity not found")
    activity_user = ActivityUser.query.filter(Activity.id == id).filter(User.username == username).filter(
        ActivityUser.using == True).first()
    if activity_user is None:
        return False, CustomError(404, 404, "user does not attend this activity")
    activity_user.using = False
    activity.attend_num = activity.attend_num - 1
    activity.remainder_num = activity.remainder_num + 1
    db.session.add(activity)
    db.session.add(activity_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, CustomError(500, 500, str(e))
    return True, None


def find_current_user_activities(username, condition=None):
    if username is None:
        return None, None, CustomError(500, 200, "username should be given")
    # activity_users = ActivityUser.query.filter(ActivityUser.using == True)
    # users = User.query.filter(User.using == True)
    activities = Activity.query.filter(Activity.using == True).outerjoin(
        ActivityUser, ActivityUser.activity_id == Activity.id).outerjoin(
        User, User.username == ActivityUser.username)
    if 'state' not in condition:
        return None, None, CustomError(500, 200, "state must be given")
    state = condition['state']
    if state == 'hasAttended':
        activities = activities.filter(ActivityUser.state == "已报名").filter(
            ActivityUser.username == username)
    elif state == 'canAttend':
        activities = activities.filter(Activity.using == True).filter(Activity.apply_state == "报名进行中").filter(
            or_(ActivityUser.state == None, ActivityUser.state == '未报名')).filter(Activity.remainder_num > 0)
    else:
        return None, None, CustomError(500, 200, "state is wrong")
    page = int(condition['_page'][0]) if '_page' in condition else 1
    per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20
    pagination = activities.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def has_attended_activity_dict(activity, username):
    try:
        attended_activity_dict = {
            'activity': {
                "id": activity.id,
                "name": activity.name,
                "teacher": activity.teacher,
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "place": activity.place,
                "state": activity.state,
                "information": activity.information,
                "all_num": activity.all_num,
                "attend_num": activity.attend_num,
                "remainder_num": activity.remainder_num,
                "term": activity.term,
                "apply_start_time": activity.apply_start_time,
                "apply_end_time": activity.apply_end_time,
                "apply_state": activity.apply_state
            },
            'activity_user': {
                'state': ActivityUser.activity_user_state(activity.id, username).state,
                'fin_state': ActivityUser.activity_user_state(activity.id, username).fin_state
            }
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return attended_activity_dict, None


def can_attend_activity_dict(activity):
    try:
        attend_activity_dict = {
            'activity': {
                "id": activity.id,
                "name": activity.name,
                "teacher": activity.teacher,
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "place": activity.place,
                "state": activity.state,
                "information": activity.information,
                "all_num": activity.all_num,
                "attend_num": activity.attend_num,
                "remainder_num": activity.remainder_num,
                "term": activity.term,
                "apply_start_time": activity.apply_start_time,
                "apply_end_time": activity.apply_end_time,
                "apply_state": activity.apply_state
            },
            'activity_user': {
                'state': '未报名',
                'fin_state': '未报名'
            }
        }
    except Exception as e:
        return None, CustomError(500, 500, str(e))
    return attend_activity_dict, None
