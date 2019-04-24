from app.utils.mysql import db
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query
from app.utils.Error import CustomError
from datetime import datetime


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), default='')
    teacher = db.Column(db.String(64), default='')
    start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    end_time = db.Column(db.TIMESTAMP, default=datetime.now)
    place = db.Column(db.String(128), default='')
    state = db.Column(db.String(16), default='')
    information = db.Column(db.String(128), default='')
    all_num = db.Column(db.Integer, default=0)
    attend_num = db.Column(db.Integer, default=0)
    remainder_num = db.Column(db.Integer, default=0)
    term = db.Column(db.String(32), default='')
    apply_start_time = db.Column(db.TIMESTAMP, default=datetime.now)
    apply_end_time = db.Column(db.TIMESTAMP, default=datetime.now)
    apply_state = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity):
        try:
            activity_dict = {
                'id': activity.id,
                'name': activity.name,
                'teacher': activity.teacher,
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'place': activity.place,
                'state': activity.state,
                'information': activity.information,
                'all_num': activity.all_num,
                'attend_num': activity.attend_num,
                'remainder_num': activity.remainder_num,
                'term': activity.term,
                'apply_start_time': activity.apply_start_time,
                'apply_end_time': activity.apply_end_time,
                'apply_state': activity.apply_state
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        name_map = {'activities': Activity}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, name_map, Activity)
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
    def get_activity(cls, id: int, unscoped: bool = False):
        activity = Activity.query
        if not unscoped:
            activity = activity.filter(Activity.using == True)
        try:
            activity = activity.filter(Activity.id == id).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        return cls.formatter(activity)

    @classmethod
    def query_activities(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        name_map = {'activities': Activity}
        query = Activity.query
        if not unscoped:
            query = query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, Activity)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_activity(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        name_map = {'activities': Activity}
        activities = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (activities, total) = process_query(activities, url_condition.filter_dict,
                                                url_condition.sort_limit_dict,
                                                url_condition.page_dict, name_map, Activity)
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
        name_map = {'activities': Activity}
        activities = Activity.query.filter(Activity.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (activities, total) = process_query(activities, url_condition.filter_dict,
                                                url_condition.sort_limit_dict,
                                                url_condition.page_dict, name_map, Activity)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default='')
    activity_id = db.Column(db.Integer, default=-1)
    state = db.Column(db.String(16), default='')
    fin_state = db.Column(db.String(16), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def formatter(cls, activity_user_user):
        try:
            activity_user_user_dict = {
                'id': activity_user_user.id,
                'username': activity_user_user.username,
                'activity_id':activity_user_user.activity_id,
                'activity_user_id': activity_user_user.id,
                'state': activity_user_user.state,
                'fin_state': activity_user_user.fin_state
            }
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return activity_user_user_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        name_map = {'activity_users': ActivityUser}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, name_map, ActivityUser)
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
    def get_activity_user(cls, activity_id: int, username: str, unscoped: bool = False):
        activity_user = ActivityUser.query
        if not unscoped:
            activity_user = activity_user.filter(ActivityUser.using == True)
        try:
            activity_user = activity_user.filter(ActivityUser.activity_id == activity_id).filter(
                ActivityUser.username == username).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        if activity_user is None:
            raise CustomError(404, 404, 'activity_user not found')
        return cls.formatter(activity_user)

    @classmethod
    def query_activity_users(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        name_map = {'activity_users': ActivityUser}
        query = ActivityUser.query
        if not unscoped:
            query = query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict,
                                           url_condition.page_dict, name_map, ActivityUser)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def delete_activity_user(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        name_map = {'activity_users': ActivityUser}
        activities = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (activities, total) = process_query(activities, url_condition.filter_dict,
                                                url_condition.sort_limit_dict,
                                                url_condition.page_dict, name_map, ActivityUser)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activities:
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
        name_map = {'activity_users': ActivityUser}
        activities = ActivityUser.query.filter(ActivityUser.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (activities, total) = process_query(activities, url_condition.filter_dict,
                                                url_condition.sort_limit_dict,
                                                url_condition.page_dict, name_map, ActivityUser)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for activity_user in activities:
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
