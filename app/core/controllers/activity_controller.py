from app.core.models.activity import Activity, ActivityUser
from app.core.controllers.user_controller import user_to_dict
from app.core.models.lesson import Term
from app.core.models.user import User
from flask_login import current_user
from sqlalchemy.sql import or_
from datetime import datetime
from app import db


def insert_activity(request_json):
    activity = Activity()
    for key, value in request_json.items():
        if key in ['state', 'apply_state', 'attend_num', 'remainder_num']:
            continue
        if hasattr(activity, key):
            setattr(activity, key, value)
    if activity.apply_start_time > activity.apply_end_time:
        return False, "apply_start_time can not be after apply_end_time"
    if activity.start_time > activity.end_time:
        return False, "start_time can not be after end_time"
    if activity.apply_end_time > activity.start_time:
        return False, "apply_end_time can not be after start_time"
    now = datetime.now()
    if str(now) > activity.apply_end_time:
        activity.apply_state = '报名已结束'
    elif str(now) < activity.apply_start_time:
        activity.apply_state = '报名未开始'
    else:
        activity.apply_state = '报名进行中'
    if str(now) > activity.end_time:
        activity.state = '活动已结束'
    elif str(now) < activity.start_time:
        activity.state = '活动未开始'
    else:
        activity.state = '活动进行中'
    activity.attend_num = 0
    activity.remainder_num = activity.all_num
    term = request_json['term'] if 'term' in request_json else Term.query.order_by(Term.name.desc()).filter(
        Term.using == True).first().name
    activity.term = term
    db.session.add(activity)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def update_activity(id, request_json):
    if id is None:
        return False, None
    activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
    if activity is None:
        return False, 'no this activity'
    for key, value in request_json.items():
        if key in ['state', 'apply_state', 'attend_num', 'remainder_num']:
            continue
        if hasattr(activity, key):
            setattr(activity, key, value)
    if activity.apply_start_time > activity.apply_end_time:
        return False, "apply_start_time can not be after apply_end_time"
    if activity.start_time > activity.end_time:
        return False, "start_time can not be after end_time"
    if activity.apply_end_time > activity.start_time:
        return False, "apply_end_time can not be after start_time"
    now = datetime.now()
    if now > activity.apply_end_time:
        activity.apply_state = '报名已结束'
    elif now < activity.apply_start_time:
        activity.apply_state = '报名未开始'
    else:
        activity.apply_state = '报名进行中'
    if now > activity.end_time:
        activity.state = '活动已结束'
    elif now < activity.start_time:
        activity.state = '活动未开始'
    else:
        activity.state = '活动进行中'
    if activity.all_num < activity.attend_num:
        return False, "all_num can not less than attend_num"
    activity.remainder_num = activity.all_num - activity.attend_num
    db.session.add(activity)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def delete_activity(id):
    activity = Activity.query.filter(Activity.id == id).first()
    if activity is None:
        return False, None
    activity.using = False
    db.session.add(activity)
    for activity_user in activity.activity_users:
        activity_user.using = False
        db.session.add(activity_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def activity_dict(activity):
    return {
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
    }


def activity_user_dict(id, user):
    return {
        "user": user_to_dict(user),
        "state": ActivityUser.activity_user_state(id, user.username).state,
        "fin_state": ActivityUser.activity_user_state(id, user.username).fin_state
    }


def find_activities(condition):
    try:
        activities = Activity.activities(condition)
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = activities.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_activity(id):
    try:
        activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    except Exception as e:
        return None, e
    if activity is None:
        return None, None
    return activity, None


def find_activity_users(id, condition):
    try:
        activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    except Exception as e:
        return None, None, e
    try:
        users = activity.activity_users
    except Exception as e:
        return None, None, e
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = users.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None


def find_activity_user(id, username):
    try:
        activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    except Exception as e:
        return None, e
    try:
        user = activity.activity_users.filter(User.username == username).first()
    except Exception as e:
        return None, e
    return user, None


def insert_activity_user(id, request_json):
    username = request_json['user']['username'] if 'user' in request_json and 'username' in request_json[
        'user'] else current_user.username
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, "no this user"
    activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
    if activity is None:
        return False, "no this activity"
    if activity.apply_state in ["报名未开始", "报名已结束"]:
        return False, activity.apply_state
    if activity.remainder_num <= 0:
        return False, "remainder_num is 0"
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
        return False, e
    return True, None


def update_activity_user(id, username, request_json):
    if username is None:
        return False, "no username"
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, "no this user"
    activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
    if activity is None:
        return False, "no this activity"
    activity_user = ActivityUser.query.filter(Activity.id == id).filter(User.username == username).filter(
        ActivityUser.using == True).first()
    if activity_user is None:
        return False, "user does not attend this activity"
    for key, value in request_json.items():
        if key in ['state', 'user']:
            continue
        if hasattr(activity_user, key):
            setattr(activity_user, key, value)
    db.session.add(activity_user)
    try:
        db.session.commit()
    except Exception as e:
        return False, e
    return True, None


def delete_activity_user(id, username):
    if username is None:
        return False, "no username"
    user = User.query.filter(User.username == username).filter(User.using == True).first()
    if user is None:
        return False, "no this user"
    activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
    if activity is None:
        return False, "no this activity"
    activity_user = ActivityUser.query.filter(Activity.id == id).filter(User.username == username).filter(
        ActivityUser.using == True).first()
    if activity_user is None:
        return False, "user does not attend this activity"
    activity_user.using = False
    activity.attend_num = activity.attend_num - 1
    activity.remainder_num = activity.remainder_num + 1
    db.session.add(activity)
    db.session.add(activity_user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, e
    return True, None


def find_current_user_activities(condition=None):
    try:
        username = condition['username'] if 'username' in condition else current_user.username
    except Exception as e:
        return None, None, e
    # activity_users = ActivityUser.query.filter(ActivityUser.using == True)
    # users = User.query.filter(User.using == True)
    activities = Activity.query.filter(Activity.using == True).outerjoin(
        ActivityUser, ActivityUser.activity_id == Activity.id).outerjoin(
        User, User.username == ActivityUser.username)
    if 'state' not in condition:
        return None, None, 'state must be gave'
    state = condition['state']
    if state == 'hasAttended':
        activities = activities.filter(ActivityUser.state == "已报名").filter(
            ActivityUser.username == username)
    if state == 'canAttend':
        activities = activities.filter(Activity.using == True).filter(Activity.apply_state == "报名进行中").filter(
            or_(ActivityUser.state == None, ActivityUser.state == '未报名'))
    page = int(condition['_page']) if '_page' in condition else 1
    per_page = int(condition['_per_page']) if '_per_page' in condition else 20
    pagination = activities.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total, None
