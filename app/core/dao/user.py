from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.mysql import db
from app import login_manager
from datetime import datetime
from flask import jsonify
from app.core.models.lesson import Term, SchoolTerm, LessonRecord
from functools import wraps
from app.utils.url_condition.url_condition_mysql import UrlCondition, process_query
from app.utils.Error import CustomError


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), index=True, default="")
    name = db.Column(db.String(64), default="")
    password_hash = db.Column(db.String(128), default="")
    sex = db.Column(db.String(16), default="男")
    email = db.Column(db.String(64), default="")
    phone = db.Column(db.String(16), default="")
    state = db.Column(db.String(8), default="")
    unit = db.Column(db.String(8), default="")
    status = db.Column(db.String(8), default="")
    prorank = db.Column(db.String(8), default="")
    skill = db.Column(db.String(16), default="")
    using = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    leader = db.Column(db.Boolean, default=False)
    guider = db.Column(db.Boolean, default=False)

    @classmethod
    def formatter(cls, user):
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
            'is_guider': user.guider,
            'is_leader': user.leader,
            'is_admin': user.admin
        }
        return user_dict

    @classmethod
    def reformatter_update(cls, data: dict):
        allow_change_list = ['name', 'sex', 'password', 'email', 'phone', 'state', 'unit', 'status', 'prorank',
                             'skill', 'group', 'work_state', 'term']
        update_data = dict()
        for key, value in data.items():
            if key in allow_change_list:
                update_data[key] = value
        return update_data

    @classmethod
    def reformatter_insert(cls, data: dict):
        return data

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user(cls, username: str):
        try:
            user = User.query.filter(User.username == username).filter(User.using == True).first()
        except Exception as e:
            return None, CustomError(500, 500, str(e))
        if user is None:
            return None, CustomError(404, 404, 'user not found')
        return cls.formatter(user), None

    @classmethod
    def query_users(cls, query_dict: dict = None):
        name_map = {'users': User, 'groups': Group, 'supervisors': Supervisor}
        query = User.query.outerjoin(Supervisor, Supervisor.username == User.username).filter(User.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, User)
        except Exception as e:
            return None, None, CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total, None

    @classmethod
    def insert_user(cls, ctx=True, data=None):
        data = cls.reformatter_insert(data)
        user = User()
        for key, value in data.items():
            if key == 'password':
                user.password = value
            if hasattr(user, key):
                setattr(user, key, value)
        role_names = data['role_names'] if 'role_names' in data else []
        role_name_dict = {'教师': 'teacher', '管理员': 'admin', '领导': 'leader'}
        for role_name in role_names:
            role_name_e = role_name_dict[role_name]
            if hasattr(user, role_name_e):
                setattr(user, role_name_e, True)
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return False, CustomError(500, 500, str(e))
        return True, None

    @classmethod
    def delete_user(cls, ctx=True, username: str = None):
        try:
            user = User.query.filter(User.username == username).first()
        except Exception as e:
            return False, CustomError(500, 500, str(e))
        if user is None:
            return False, CustomError(404, 404, 'user not found')
        user.using = False
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return False, CustomError(500, 500, str(e))
        return True, None

    @classmethod
    def update_user(cls, ctx=True, username: str = None, data: dict = None):
        data = cls.reformatter_update(data)
        try:
            user = User.query.filter(User.username == username).filter(User.using == True).first()
        except Exception as e:
            return False, CustomError(500, 500, str(e))
        if user is None:
            return False, CustomError(404, 404, 'user not found')
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.add(user)
        if ctx:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return False, CustomError(500, 500, str(e))
        return True, None


login_manager.anonymous_user = AnonymousUserMixin


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(64), unique=True, default="")
    leader_name = db.Column(db.String(64), default="")
    using = db.Column(db.Boolean, default=True)

    @classmethod
    def formatter(cls, group):
        group_dict = {
            'name': group.name,
            'leader_name': group.leader_name
        }
        return group_dict

    @property
    def leader(self):
        return User.query.join(Group, User.username == Group.leader_name).filter(Group.id == self.id).filter(
            Group.using == True).first()

    @classmethod
    def query_groups(cls, query_dict: dict = None):
        name_map = {'groups': Group}
        url_condition = UrlCondition(query_dict)
        query = Group.query.filter(Group.using == True)
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, Group)
        except Exception as e:
            return None, None, CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total, None


class Supervisor(db.Model):
    __tablename__ = 'supervisors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(64), default="")
    group = db.Column(db.String(16), default="")
    work_state = db.Column(db.String(8), default="")
    term = db.Column(db.String(32), default="")
    using = db.Column(db.Boolean, default=True)
    grouper = db.Column(db.Boolean, default=False)
    main_grouper = db.Column(db.Boolean, default=False)

    @staticmethod
    def supervisors(condition):
        name_map = {"supervisors": Supervisor}
        url_condition = UrlCondition(condition)
        user_query = User.query.filter(User.using == True)
        user_query = process_query(user_query, url_condition, name_map, User)
        supervisors = Supervisor.query.filter(Supervisor.username.in_([user.username for user in user_query])).filter(
            Supervisor.using == True)
        for key, value in condition:
            if hasattr(Supervisor, key):
                supervisors = supervisors.filter(getattr(Supervisor, key) == value)
        return supervisors

    @classmethod
    def formatter(cls, supervisor):
        supervisor_dict = {
            'group': supervisor.group,
            'is_grouper': supervisor.grouper,
            'is_main_grouper': supervisor.main_grouper,
            'work_state': supervisor.work_state,
            'term': supervisor.term
        }
        return supervisor_dict

    @classmethod
    def query_supervisors(cls, query_dict: dict):
        name_map = {"supervisors": Supervisor}
        query = Supervisor.query.join(User, User.username == Supervisor.username).filter(User.using == True).filter(
            Supervisor.using == True)
        url_condition = UrlCondition(query_dict)
        try:
            (query, total) = process_query(query, url_condition.filter_dict,
                                           url_condition.sort_limit_dict, url_condition.page_dict,
                                           name_map, Supervisor)
        except Exception as e:
            return None, None, CustomError(500, 500, str(e))
        return [cls.formatter(data) for data in query], total, None

    @classmethod
    def get_supervisor(cls, username: str = None, term: str = None):
        try:
            supervisor = Supervisor.query.filter(Supervisor.username == username).filter(
                Supervisor.using == True).filter(Supervisor.term == term).first()
        except Exception as e:
            return None, CustomError(500, 500, str(e))
        if supervisor is None:
            return None, CustomError(404, 404, 'user not found')
        return cls.formatter(supervisor), None

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
                return False, CustomError(500, 500, str(e))
        return True, None


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(255), default="")
    username = db.Column(db.String(64), default="")
    detail = db.Column(db.String(1023), default="")
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now)
    using = db.Column(db.Boolean, default=True)

    @staticmethod
    def events(condition):
        name_map = {"events": Event}
        url_condition = UrlCondition(condition)
        query = Event.query.filter(Event.using == True)
        query = process_query(query, url_condition, name_map, Event)
        return query


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return jsonify(status="fail", data=[], reason="no permission")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
