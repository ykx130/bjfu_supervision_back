from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.mysql import db
from app import login_manager
from datetime import datetime
from flask import jsonify
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query, count_query, page_query
from app.utils.Error import CustomError
from app.utils.misc import convert_string_to_datetime, convert_datetime_to_string


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), index=True, default='')
    name = db.Column(db.String(64), default='')
    password_hash = db.Column(db.String(128), default='')
    sex = db.Column(db.String(16), default='男')
    email = db.Column(db.String(64), default='')
    phone = db.Column(db.String(16), default='')
    state = db.Column(db.String(8), default='')
    unit = db.Column(db.String(8), default='')
    status = db.Column(db.String(8), default='')
    prorank = db.Column(db.String(8), default='')
    skill = db.Column(db.String(16), default='')
    using = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_leader = db.Column(db.Boolean, default=False)
    is_guider = db.Column(db.Boolean, default=False)
    is_reader = db.Column(db.Boolean, default=False)
    is_develop = db.Column(db.Boolean, default=False)
    start_working=db.Column(db.Date, default='1000-01-01')


    @classmethod
    def formatter(cls, user):
        if user is None:
            return None
        if user.start_working is None:
            default_time='1000-01-01'
            user.start_working= datetime.strptime(default_time,'%Y-%m-%d')
        user_dict = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'sex': user.sex,
            'email': user.email,
            'phone': user.phone,
            'state': user.state,
            'unit': user.unit,
            'status': user.status,
            'prorank': user.prorank,
            'skill': user.skill,
            'is_guider': user.is_guider,
            'is_leader': user.is_leader,
            'is_admin': user.is_admin,
            'is_reader': user.is_reader,
            'is_develop':user.is_develop,
            'start_working':str(user.start_working.strftime('%Y-%m-%d'))
        }
        return user_dict

    @classmethod
    def reformatter_update(cls, data: dict):
        allow_change_list = ['name', 'sex', 'password', 'email', 'phone', 'state', 'unit', 'status', 'prorank',
                             'skill', 'group_name', 'work_state', 'term', 'is_admin', 'is_leader', 'is_guider','is_reader','is_develop','start_working']
        update_data = dict()
        for key, value in data.items():
            if key in allow_change_list:
                update_data[key] = value
        return update_data

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = User.query
        if not unscoped:
            query = query.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, User)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def login(cls, username: str, password: str):
        user = User.query.filter(User.username == username).filter(User.using == True).first()
        if user is None or not check_password_hash(user.password_hash, password):
            raise CustomError(401, 401, '用户名或密码错误')
        login_user(user, remember=False)

    @classmethod
    def logout(cls):
        logout_user()

    @classmethod
    def get_user(cls, query_dict: dict, unscoped=False):
        user = User.query
        if not unscoped:
            user = user.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            user = process_query(user, url_condition.filter_dict, url_condition.sort_limit_dict,
                                 User).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(user)

    @classmethod
    def query_users(cls, query_dict: dict = None, unscoped=False):
        if query_dict is None:
            query_dict = {}
        query = User.query
        if not unscoped:
            query = query.filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, User)
            (users, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(user) for user in users], total

    @classmethod
    def insert_user(cls, ctx=True, data=None):
        if data is None:
            raise CustomError(500, 200, 'data must be given')
        data = cls.reformatter_insert(data)
        user = User()
        for key, value in data.items():
            if key == 'password':
                user.password = value
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_user(cls, ctx=True, username: str = None):
        try:
            user = User.query.filter(User.username == username).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        user.using = False
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_user(cls, ctx=True, username: str = None, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_update(data)
        try:
            user = User.query.filter(User.username == username).filter(User.using == True).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for key, value in data.items():
            if hasattr(user, key) or key == 'password':
                setattr(user, key, value)
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise CustomError(500, 500, str(e))
        return True


login_manager.anonymous_user = AnonymousUserMixin


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    group_name = db.Column(db.String(64), unique=True, default='')
    leader_name = db.Column(db.String(64), default='')
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, group):
        if group is None:
            return None
        group_dict = {
            'group_name': group.group_name,
            'leader_name': group.leader_name
        }
        return group_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Group.query
        if not unscoped:
            query = query.filter(Group.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Group)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def get_group(cls, group_name: str):
        try:
            group = Group.query.filter(Group.using == True).filter(Group.name == group_name).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(group)

    @classmethod
    def query_groups(cls, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        url_condition = UrlCondition(query_dict)
        query = Group.query.filter(Group.using == True)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Group)
            (groups, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total

    @classmethod
    def update_group(cls, ctx=True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        url_condition = UrlCondition(query_dict)
        query = Group.query.filter(Group.using == True)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Group)
            (groups, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for group in groups:
            for key, value in data.items():
                if hasattr(group, key):
                    setattr(group, key, value)
            db.session.add(group)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise CustomError(500, 500, str(e))
        return True


class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default='')
    name = db.Column(db.String(64), default='')
    group_name = db.Column(db.String(16), default='')
    work_state = db.Column(db.String(8), default='')
    term = db.Column(db.String(32), default='')
    using = db.Column(db.Boolean, default=True)
    grouper = db.Column(db.Boolean, default=False)
    unit = db.Column(db.String)
    main_grouper = db.Column(db.Boolean, default=False)

    @classmethod
    def formatter(cls, supervisor):
        if supervisor is None:
            return None
        supervisor_dict = {
            "id": supervisor.id,
            'group_name': supervisor.group_name,
            'username': supervisor.username,
            'is_grouper': supervisor.grouper,
            'is_main_grouper': supervisor.main_grouper,
            'work_state': supervisor.work_state,
            'term': supervisor.term,
            'name': supervisor.name
        }
        return supervisor_dict

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Supervisor.query
        if not unscoped:
            query = query.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Supervisor)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total

    @classmethod
    def query_supervisors(cls, query_dict: dict, unscoped: bool = False):
        query = Supervisor.query
        if not unscoped:
            query = query.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Supervisor)
            (supervisors, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(supervisor) for supervisor in supervisors], total

    @classmethod
    def get_supervisor(cls, query_dict: dict, unscoped: bool = False):
        supervisor = Supervisor.query
        if not unscoped:
            supervisor = supervisor.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            supervisor = process_query(supervisor, url_condition.filter_dict, url_condition.sort_limit_dict,
                                       Supervisor).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(supervisor)

    @classmethod
    def get_supervisor_by_id(cls, query_dict: dict, unscoped: bool = False):
        supervisor = Supervisor.query
        if not unscoped:
            supervisor = supervisor.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            supervisor = process_query(supervisor, url_condition.filter_dict, url_condition.sort_limit_dict,
                                       Supervisor).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(supervisor)

    @classmethod
    def insert_supervisor(cls, ctx=True, data=None):
        supervisor = Supervisor()
        for key, value in data.items():
            if hasattr(supervisor, key):
                setattr(supervisor, key, value)
        db.session.add(supervisor)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def delete_supervisor(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Supervisor.query.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Supervisor)
            (supervisors, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for supervisor in supervisors:
            supervisor.using = False
            db.session.add(supervisor)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_supervisor(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        query = Supervisor.query.filter(Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Supervisor)
            (supervisors, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for supervisor in supervisors:
            for key, value in data.items():
                if hasattr(supervisor, key):
                    setattr(supervisor, key, value)
            db.session.add(supervisor)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(255), default='')
    username = db.Column(db.String(64), default='')
    detail = db.Column(db.String(1023), default='')
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, event):
        if event is None:
            return None
        event_dict = {
            'id': event.id,
            'username': event.username,
            'detail': event.detail,
            'timestamp': str(event.timestamp),
            'using': event.using
        }
        return event_dict

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @classmethod
    def reformatter_update(cls, data: dict):
        return data

    @classmethod
    def count(cls, query_dict: dict, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Event.query
        if not unscoped:
            query = query.filter(Event.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            total = count_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Event)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return total
    @classmethod
    def get_event(cls, query_dict: dict, unscoped: bool = False):
        event = Event.query
        if not unscoped:
            event = event.filter(Event.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            event = process_query(event, url_condition.filter_dict, url_condition.sort_limit_dict,
                                  Event).first()
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return cls.formatter(event)

    @classmethod
    def insert_event(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        data = cls.reformatter_insert(data)
        event = Event()
        for key, value in data.items():
            if hasattr(event, key):
                setattr(event, key, value)
        db.session.add(event)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def query_events(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        query = Event.query
        if not unscoped:
            query = query.filter(Event.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Event)
            (events, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        return [cls.formatter(event) for event in events], total

    @classmethod
    def delete_event(cls, ctx: bool = True, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        query = Event.query.filter(Event.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Event)
            (events, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for event in events:
            event.using = False
            db.session.add(event)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def update_event(cls, ctx: bool = True, query_dict: dict = None, data: dict = None):
        if data is None:
            data = {}
        if query_dict is None:
            query_dict = {}
        data = cls.reformatter_update(data)
        query = Event.query.filter(Event.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            query = process_query(query, url_condition.filter_dict, url_condition.sort_limit_dict, Event)
            (events, total) = page_query(query, url_condition.page_dict)
        except Exception as e:
            raise CustomError(500, 500, str(e))
        for event in events:
            for key, value in data.items():
                if hasattr(event, key):
                    setattr(event, key, value)
            db.session.add(event)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                raise CustomError(500, 500, str(e))
        return True


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return jsonify(status='fail', data=[], reason='no permission')
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
