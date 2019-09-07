from functools import wraps
from app.core.controller.user import AuthController, SupervisorController
from app.core.services.term import TermService
from flask import jsonify, request, g
from app.utils import args_to_dict


class Filter(object):

    @classmethod
    def filter_permission(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """

                :param args:
                :param kwargs:
                :return:
                """
                user = AuthController.get_current_user()
                query_dict = dict()
                query_dict.update(kwargs)

                if user is not None:
                    username = user.get('username')
                    user_id = user.get('id')
                    role_names = user.get('role_names', list())
                    is_supervisor = ('督导' in role_names)
                    is_grouper = ('小组长' in role_names)
                    is_main_grouper = ('大组长' in role_names)
                    is_admin = ('管理员' in role_names)
                    is_leader = ('学院领导' in role_names)

                    term = query_dict.get('term')
                    if term is None:
                        term = TermService.get_now_term()['name']
                        query_dict.update({'term': term})
                    if is_admin:
                        query_dict = query_dict
                    elif is_leader:
                        query_dict.update({'unit': [user['unit']]})
                    elif is_supervisor:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group_name')
                        if is_main_grouper:
                            query_dict = query_dict
                        elif is_grouper:
                            supervisors, _ = SupervisorController.query_supervisors(
                                query_dict={'group_name': [group], 'term': term})
                            usernames = [supervisor.get('username') for supervisor in supervisors]
                            query_dict.update(
                                {'group_name': [group], 'username': usernames})
                        else:
                            query_dict.update(
                                {'group_name': [group], 'username': [username], 'user_id': [user_id]})
                    else:
                        query_dict.update({'username': [username], 'user_id': [user_id]})
                print(query_dict)
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func

    @classmethod
    def filter_permission_mongo(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                领导只过滤自己院的, 督导过滤自己院和自己组的
                :param args:
                :param kwargs:
                :return:
                """
                user = AuthController.get_current_user()
                query_dict = dict()
                query_dict.update(kwargs)
                if user is not None:
                    username = user.get('username')
                    role_names = user.get('role_names', list())
                    is_supervisor = ('督导' in role_names)
                    is_admin = ('管理员' in role_names)
                    is_grouper = ('小组长' in role_names)
                    is_main_grouper = ('大组长' in role_names)
                    is_leader = ('学院领导' in role_names)
                    term = query_dict.get('term')
                    if term is None:
                        term = TermService.get_now_term()['name']
                        query_dict.update({'meta.term': term})
                    if is_admin:
                        pass
                    elif is_leader:
                        query_dict.update({'meta.lesson.lesson_teacher_unit':user.get('unit')})
                    elif is_supervisor:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group_name')
                        if is_main_grouper:
                            query_dict = query_dict
                        elif is_grouper:
                            supervisors, _ = SupervisorController.query_supervisors(query_dict={'group_name': [group]})
                            usernames = [supervisor.get('username') for supervisor in supervisors]
                            query_dict.update(
                                {'meta.guider_group': group, 'meta.guider': usernames, 'meta.term': term})
                        else:
                            query_dict.update(
                                {'meta.guider_group': group, 'meta.guider': username, 'meta.term': term})
                print(query_dict)
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func



class NewFilter(object):

    @classmethod
    def filter_permission(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """

                :param args:
                :param kwargs:
                :return:
                """
                user = AuthController.get_current_user()
                current_role = request.args.get('current_role')
                query_dict = {}
                pass
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func

    @classmethod
    def filter_permission_mongo(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                领导只过滤自己院的, 督导过滤自己院和自己组的
                :param args:
                :param kwargs:
                :return:
                """
                user = AuthController.get_current_user()
                current_role = request.args.get('current_role')
                query_dict = {}
                if current_role == "大组长":
                    pass
                elif current_role == "小组长":
                    query_dict['group'] = ''
                pass

                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func
