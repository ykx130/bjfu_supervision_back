from app.utils.mysql import db
from datetime import datetime
from app.utils.Error import CustomError
from app.core.models.user import User
from app.core.models.lesson import Term

from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default="")
    teacher = db.Column(db.String(64), default="")
    start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    end_time = db.Column(db.TIMESTAMP, default=datetime.now)
    place = db.Column(db.String(128), default="")
    state = db.Column(db.String(16), default="")
    information = db.Column(db.String(128), default="")
    all_num = db.Column(db.Integer, default=0)
    attend_num = db.Column(db.Integer, default=0)
    remainder_num = db.Column(db.Integer, default=0)
    term = db.Column(db.String(32), default="")
    apply_start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    apply_end_time = db.Column(db.TIMESTAMP, default=datetime.now)
    apply_state = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def insert_activity(cls, data):
        """
        插入活动.
        :param data: 活动
        :return:s
        """
        activity = cls()
        for key, value in data.items():
            if key in ['state', 'apply_state', 'attend_num', 'remainder_num']:
                continue
            if hasattr(activity, key):
                setattr(activity, key, value)
        if activity.apply_start_time > activity.apply_end_time:
            raise CustomError(code=500, status_code=500, err_info="apply_start_time can not be after apply_end_time")
        if activity.start_time > activity.end_time:
            raise CustomError(code=500, status_code=500, err_info="start_time can not be after end_time")
        if activity.apply_end_time > activity.start_time:
            raise CustomError(code=500, status_code=500, err_info="apply_end_time can not be after start_time")
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
        term = data['term'] if 'term' in data else Term.query.order_by(Term.name.desc()).filter(
            Term.using == True).first().name
        activity.term = term
        try:
            db.session.add(activity)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))
        return activity

    @classmethod
    def update_activity(cls, id, data):
        """
        更新数据
        :param data:
        :return:
        """
        if id is None:
            raise CustomError(404, 404, 'activity not found')
        activity = Activity.query.filter(Activity.id == id).filter(Activity.using == True).first()
        if activity is None:
            return False,
        for key, value in data.items():
            if key in ['state', 'apply_state', 'attend_num', 'remainder_num']:
                continue
            if hasattr(activity, key):
                setattr(activity, key, value)
        if activity.apply_start_time > activity.apply_end_time:
            raise CustomError(code=500, status_code=500, err_info="apply_start_time can not be after apply_end_time")
        if activity.start_time > activity.end_time:
            raise CustomError(code=500, status_code=500, err_info="start_time can not be after end_time")
        if activity.apply_end_time > activity.start_time:
            raise CustomError(code=500, status_code=500, err_info="apply_end_time can not be after start_time")
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
            raise CustomError(500, 200, "all_num can not less than attend_num")
        activity.remainder_num = activity.all_num - activity.attend_num
        db.session.add(activity)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))
        return activity

    @classmethod
    def delete_activity(cls, id):
        """
        删除
        :param id:
        :return:
        """
        activity = Activity.query.filter(Activity.id == id).first()
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        activity.using = False
        db.session.add(activity)
        for activity_user in activity.activity_users:
            activity_user.using = False
            db.session.add(activity_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CustomError(500, 500, str(e))
        return activity

    @classmethod
    def find_activities(cls, condition):

        name_map = {'activities': Activity, 'activity_users': ActivityUser, 'users': User}
        url_condition = UrlCondition(condition)
        query = Activity.query.outerjoin(ActivityUser, ActivityUser.activity_id == Activity.id).outerjoin(User,
                                                                                                          User.username == ActivityUser.username).filter(
            Activity.using == True)
        activities = process_query(query, url_condition, name_map, Activity)

        page = int(condition['_page'][0]) if '_page' in condition else 1
        per_page = int(condition['_per_page'][0]) if '_per_page' in condition else 20

        pagination = activities.paginate(page=int(page), per_page=int(per_page), error_out=False)
        return pagination.items, pagination.total

    @classmethod
    def get_activate(cls, id):
        try:
            activity = Activity.query.filter(Activity.using == True).filter(Activity.id == id).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity


class ActivityUser(db.Model):
    __tablename__ = 'activity_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    activity_id = db.Column(db.Integer, default=-1)
    state = db.Column(db.String(16), default="")
    fin_state = db.Column(db.String(16), default="")
    using = db.Column(db.Boolean, default=True)

    @property
    def activity(self):
        return Activity.get_activate(self.id)

    @property
    def user(self):
        return {}

    @classmethod
    def find_activity_users(cls, id, condition):
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

