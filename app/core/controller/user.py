import app.core.dao as dao
from app.utils import CustomError, db
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash


class SchoolTerm():
    def __init__(self, term_name: str = None):
        self.term_name = term_name

    def __add__(self, other):
        term_parts = self.term_name.split('-')
        term_future = 2 if (int(term_parts[2]) + other) % 2 == 0 else 1
        years = other / 2 if (int(term_parts[2]) == 1) else other / 2 + 1
        begin_year = int(int(term_parts[0]) + years)
        end_year = int(int(term_parts[1]) + years)
        return SchoolTerm(term_name='-'.join([str(begin_year), str(end_year), str(term_future)]))


class AuthController():
    @classmethod
    def login(cls, username: str, password: str):
        if username is None or password is None:
            raise CustomError(401, 401, 'username or password can not be null')
        try:
            dao.User.login(username=username, password=password)
        except Exception as e:
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, err_info=str(e))
        return True

    @classmethod
    def logout(cls):
        try:
            dao.User.logout()
        except Exception as e:
            raise CustomError(500, 500, e)

    @classmethod
    def get_current_user(cls):
        user = UserController.get_user(username=current_user.username)
        return user


class UserController():

    @classmethod
    def role_list(cls, user: dict, term: str):
        role_list_dict = {'is_grouper': '小组长', 'is_main_grouper': '大组长', 'is_admin': '管理员', 'is_leader': '领导',
                          'is_guider': '督导'}
        role_names = ['教师']
        for role_name_e, role_name_c in role_list_dict.items():
            if user[role_name_e] is True:
                role_names.append(role_name_c)
        if user['is_guider']:
            supervisor = dao.Supervisor.get_supervisor(user['username'], term)
            for role_name_e, role_name_c in role_list_dict.items():
                if supervisor[role_name_e] is True:
                    role_names.append(role_name_c)
        return role_names

    @classmethod
    def formatter(cls, user: dict):
        term = dao.Term.get_now_term()['name']
        role_names = cls.role_list(user, term)
        user['role_names'] = role_names
        if user['is_guider']:
            supervisor = dao.Supervisor.get_supervisor(user['username'], term)
            user['guider'] = supervisor
        return user

    @classmethod
    def reformatter(cls, data: dict):
        return data

    @classmethod
    def query_users(cls, query_dict: dict = None, unscoped=False):
        if query_dict is None:
            query_dict = dict()
        (users, num) = dao.User.query_users(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(user) for user in users], num

    @classmethod
    def get_user(cls, username, unscoped=False):
        user = dao.User.get_user(username=username, unscoped=unscoped)
        return cls.formatter(user)

    @classmethod
    def insert_user(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        data = cls.reformatter(data)
        username = data.get('username', None)
        if username is None:
            raise CustomError(500, 200, 'username should be given')
        try:
            dao.User.get_user(username=username)
        except CustomError as e:
            if e is not None:
                raise CustomError(500, 200, 'username has been used')
            elif e is not None and e.status_code != 404:
                raise e
        try:
            dao.User.insert_user(ctx=ctx, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        role_names = data.get('role_names', [])
        if '督导' in role_names:
            send_kafka_message(topic='user_service',
                               method='add_supervisor',
                               usernames=[username])
        return True

    @classmethod
    def update_user(cls, ctx: bool = True, username: str = '', data: dict = None):
        if data is None:
            data = dict()
        try:
            data['term'] = data.get('term', dao.Term.get_now_term()['name'])
            if username is None:
                raise CustomError(500, 500, 'username or role_names should be given')

            term = data['term']
            user = dao.User.get_user(username)
            dao.User.update_user(ctx=False, username=username, data=data)

            # supervisor role_name 变更
            role_names = list(set(data.get('role_names', [])))
            old_role_names = cls.role_list(user=user, term=term)
            new_role_names = list(set(role_names) - set(old_role_names))
            del_role_names = list(set(old_role_names) - set(role_names))
            if '督导' in del_role_names:
                del_role_names.remove('督导')
                SupervisorController.delete_supervisor(ctx=False, username=username, term=term)
            elif '督导' in new_role_names:
                new_role_names.remove('督导')
                SupervisorController.insert_supervisor(ctx=False, data=data)
            if '小组长' in del_role_names:
                del_role_names.remove('小组长')
                supervisor = dao.Supervisor.get_supervisor(username=username, term=term)
                group_name = data['group_name'] if 'group_name' in data else supervisor['group']
                SupervisorController.update_grouper(ctx=False, username=username, term=term,
                                                    group_name=group_name, role_name='grouper', add=False)
            elif '小组长' in new_role_names:
                new_role_names.remove('小组长')
                supervisor = dao.Supervisor.get_supervisor(username=username, term=term)
                group_name = data.get('group_name', supervisor['group'])
                (groupers, num) = dao.Supervisor.query_supervisors(
                    query_dict={'term_gte': [term], 'grouper': [True], 'group': [group_name]})
                if num > 0:
                    grouper = groupers[0]
                    SupervisorController.update_grouper(ctx=False, username=grouper['username'], term=term,
                                                        group_name=group_name, role_name='小组长', add=False)
                SupervisorController.update_grouper(ctx=False, username=username, term=term, group_name=group_name,
                                                    role_name='grouper', add=True)
            if '大组长' in del_role_names:
                del_role_names.remove('大组长')
                SupervisorController.update_grouper(ctx=False, username=username, term=term, role_name='main_grouper',
                                                    add=False)
            elif '大组长' in new_role_names:
                new_role_names.remove('大组长')
                (groupers, num) = dao.Supervisor.query_supervisors(
                    query_dict={'term_gte': [term], 'grouper': [True], 'main_grouper': [True]})
                if num > 0:
                    grouper = groupers[0]
                    SupervisorController.update_grouper(ctx=False, username=grouper['username'], term=term,
                                                        role_name='main_grouper', add=False)
                SupervisorController.update_grouper(ctx=False, username=username, term=term, role_name='main_grouper',
                                                    add=True)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, err_info=str(e))
        return True

    @classmethod
    def delete_user(cls, ctx: bool = True, username: str = ''):
        try:
            dao.User.delete_user(ctx=ctx, username=username)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True


class SupervisorController():
    @classmethod
    def query_supervisors(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        (supervisors, _) = dao.Supervisor.query_supervisors(query_dict=query_dict, unscoped=unscoped)
        usernames = [supervisor['username'] for supervisor in supervisors]
        (users, num) = UserController.query_users(query_dict={'username': usernames}, unscoped=unscoped)
        return users, num

    @classmethod
    def query_supervisors_expire(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = dict()
        term = query_dict.get('term', [])
        if len(term) == 0:
            term = [dao.Term.get_now_term()['name']]
        if 'term' in query_dict:
            del query_dict['term']
        new_term = [(SchoolTerm(term[0]) + 1).term_name]

        all_query_dict = query_dict
        all_query_dict['term'] = term
        all_query_dict['_per_page'] = [100000]
        all_usernames = list()
        (all_supervisors, num) = dao.Supervisor.query_supervisors(query_dict=all_query_dict, unscoped=unscoped)
        for supervisor in all_supervisors:
            all_usernames.append(supervisor['username'])

        can_query_dict = query_dict
        can_query_dict['term'] = new_term
        can_query_dict['_per_page'] = [100000]
        can_usernames = list()
        (can_supervisors, num) = dao.Supervisor.query_supervisors(query_dict=can_query_dict, unscoped=unscoped)
        for supervisor in can_supervisors:
            can_usernames.append(supervisor['username'])

        expire_usernames = list(set(all_usernames) - set(can_usernames))
        query_dict['username'] = expire_usernames
        (users, num) = UserController.query_users(query_dict=query_dict, unscoped=False)
        return users, num

    @classmethod
    def delete_supervisor(cls, ctx: bool = True, username: str = '', term: str = None):
        if term is None:
            term = dao.Term.get_now_term()['name']
        try:
            dao.User.update_user(ctx=False, username=username, data={'guider': False})
            dao.Supervisor.delete_supervisor(ctx=False, query_dict={'username': [username], 'term_gte': [term]})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def insert_supervisor(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        username = data.get('username', None)
        user = dao.User.get_user(username)
        term = data.get('term', None)
        if username is None:
            raise CustomError(500, 200, 'username should be given')
        if term is None:
            term = dao.Term.get_now_term()['name']
        try:
            dao.User.update_user(ctx=False, username=username, data={'guider': True})
            school_term = SchoolTerm(term)
            for i in range(0, 4):
                data['term'] = school_term.term_name
                dao.Supervisor.insert_supervisor(ctx=False, data=data)
                school_term = school_term + 1
                lesson_record_data = {'username': username, 'term': term, 'group_name': data['group_name'],
                                      'name': user['name']}
                dao.LessonRecord.insert_lesson_record(ctx=False, data=lesson_record_data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, err_info=str(e))
        return True

    @classmethod
    def update_grouper(cls, ctx: bool = True, username: str = '', term: str = '', group_name: str = '',
                       role_name: str = '', add: bool = False):
        (supervisors, num) = dao.Supervisor.query_supervisors(query_dict={'username': [username], 'term_gte': [term]})
        if num == 0:
            raise CustomError(500, 200, 'user must be supervisor')
        try:
            dao.Supervisor.update_supervisor(ctx=False, query_dict={'username': [username], 'term_gte': [term]},
                                             data={role_name: add, 'group': group_name})
            if add:
                dao.Group.update_group(ctx=False, query_dict={'name': [group_name]}, data={'leader_name': [username]})
            else:
                dao.Group.update_group(ctx=False, query_dict={'name': [group_name]}, data={'leader_name': ['']})
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, err_info=str(e))
        return True

    @classmethod
    def batch_renewal(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = dict()
        usernames = data.get('usrnames', None)
        term = data.get('term', None)
        if usernames is None:
            raise CustomError(500, 500, 'usernames should be given')
        if term is None:
            term = dao.Term.get_now_term()['name']
        try:
            for username in usernames:
                school_term = SchoolTerm(term)
                supervisor = dao.Supervisor.get_supervisor(username=username, term=term)
                for i in range(0, 4):
                    school_term = school_term + 1
                    data['term'] = school_term.term_name
                    data['username'] = username
                    data['group'] = supervisor['group']
                    dao.Supervisor.insert_supervisor(ctx=False, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        return True

    @classmethod
    def get_supervisor_num(cls, query_dict: dict = None):
        if query_dict is None:
            query_dict = dict()
        term = query_dict.get('term', dao.Term.get_now_term()['name'])
        (supervisors, num) = dao.Supervisor.query_supervisors(query_dict={'_per_page': [100000], 'term': [term]})
        return num


class GroupController():
    @classmethod
    def formatter(cls, group: dict):
        leader = dao.User.get_user(username=group['leader_name'], unscoped=True)
        return {'name': group['name'], 'leader': leader}

    @classmethod
    def query_groups(cls, query_dict):
        groups, num = dao.Group.query_groups(query_dict)
        return [cls.formatter(group) for group in groups], num
