from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.Error import CustomError
from app.utils.misc import convert_string_to_datetime, convert_datetime_to_string
from datetime import datetime


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    title = db.Column(db.String(64), default='')
    presenter = db.Column(db.String(64), default='')
    module = db.Column(db.String(64), default='')
    start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    place = db.Column(db.String(128), default='')
    apply_state = db.Column(db.String(16), default='')
    organizer = db.Column(db.String(64), default='')
    all_num = db.Column(db.Integer, default=0)
    attend_num = db.Column(db.Integer, default=0)
    remainder_num = db.Column(db.Integer, default=0)
    term = db.Column(db.String(32), default='')
    period = db.Column(db.Integer, default=0)
    is_obligatory=db.Column(db.Boolean, default=False)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity):
        if activity is None:
            return None
        try:
            activity_dict = {
                'id': activity.id,
                'title': activity.title,
                'presenter': activity.presenter,
                'module':activity.module,
                'start_time': convert_datetime_to_string(activity.start_time),
                'place': activity.place,
                'apply_state': activity.apply_state,
                'organizer': activity.organizer,
                'all_num':activity.all_num,
                'attend_num': activity.attend_num,
                'remainder_num': activity.remainder_num,
                'term': activity.term,
                'period':activity.period,
                'is_obligatory': activity.is_obligatory
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, Activity)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_activity(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        activity = Activity()
        for key, value in data.items():
            if hasattr(Activity, key):
                setattr(activity, key, value)
        db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_activity(cls, query_dict: dict, unscoped: bool = False):
        activity = Activity.query
        if not unscoped:
            activity = activity.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            activity = process_query(activity, url_condition.filter_dict, url_condition.sort_limit_dict,
                                     Activity).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(activity)

    @classmethod
    def query_activities(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(activity) for activity in activities], total

    @classmethod
    def delete_activity(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity in activities:
            activity.using = False
            db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_activity(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, Activity)
            (activities, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity in activities:
            for key, value in data.items():
                if hasattr(activity, key):
                    setattr(activity, key, value)
            db.session.add(activity)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class ActivityUser(db.Model):
    __tablename__ = 'activity_users'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, index=True)
    username = db.Column(db.String(64), default='')
    activity_id = db.Column(db.Integer, default=-1)
    state = db.Column(db.String(16), default='')
    fin_state = db.Column(db.String(16), default='')
    activity_type = db.Column(db.String(64), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity_user_user):
        if activity_user_user is None:
            return None
        try:
            activity_user_user_dict = {
                'id': activity_user_user.id,
                'username': activity_user_user.username,
                'activity_id': activity_user_user.activity_id,
                # 'activity_user_id': activity_user_user.id,
                'state': activity_user_user.state,
                'fin_state': activity_user_user.fin_state,
                'activity_type':activity_user_user.activity_type
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_user_user_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict,
                                url_condition.sort_limit_dict, ActivityUser)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def insert_activity_user(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        activity_user = ActivityUser()
        for key, value in data.items():
            if hasattr(ActivityUser, key):
                setattr(activity_user, key, value)
        db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_activity_user(cls, query_dict: dict, unscoped: bool = False):
        activity_user = ActivityUser.query
        if not unscoped:
            activity_user = activity_user.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            activity_user = process_query(activity_user, url_condition.filter_dict, url_condition.sort_limit_dict,
                                          ActivityUser).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(activity_user)

    @classmethod
    def query_activity_users(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(activity_user) for activity_user in activity_users], total

    @classmethod
    def delete_activity_user(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activity_users:
            activity_user.using = False
            db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_activity_user(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(
                query, url_condition.filter_dict, url_condition.sort_limit_dict, ActivityUser)
            (activity_users, total) = page_query(
                query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activity_users:
            for key, value in data.items():
                if hasattr(activity_user, key):
                    setattr(activity_user, key, value)
            db.session.add(activity_user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True
