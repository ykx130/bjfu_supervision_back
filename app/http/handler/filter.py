from functools import wraps
from app.core.controller.user import AuthController, SupervisorController
from flask import jsonify, request, g
from app.utils import args_to_dict


class Filter(object):

    @classmethod
    def filter_permission(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user = AuthController.get_current_user()
                query_dict = dict()
                query_dict.update(kwargs)
                if user is None:
                    username = user.get('username')
                    user_id = user.get('id')
                    role_names = user.get('role_names', list())
                    is_supervisor = ('督导' in role_names)
                    is_grouper = ('小组长' in role_names)
                    is_main_grouper = ('大组长' in role_names)
                    query_dict = args_to_dict(request.args)
                    if is_supervisor:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group')
                        if is_main_grouper:
                            query_dict = query_dict
                        elif is_grouper:
                            supervisors = SupervisorController.query_supervisors(query_dict={'group': [group]})
                            usernames = [supervisor.username for supervisor in supervisors]
                            query_dict.update(
                                {'group_name': [group], 'group': [group], 'assign_group': [group],
                                 'username': [usernames]})
                        else:
                            query_dict.update(
                                {'group_name': [group], 'group': [group], 'username': [username], 'user_id': [user_id]})
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func

    @classmethod
    def filter_permission_mongo(cls):
        def filter_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user = AuthController.get_current_user()
                query_dict = dict()
                query_dict.update(kwargs)
                if user is None:
                    username = user.get('username')
                    user_id = user.get('id')
                    role_names = user.get('role_names', list())
                    is_supervisor = ('督导' in role_names)
                    is_grouper = ('小组长' in role_names)
                    is_main_grouper = ('大组长' in role_names)
                    query_dict = args_to_dict(request.args)
                    if is_supervisor:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group')
                        if is_main_grouper:
                            query_dict = query_dict
                        elif is_grouper:
                            supervisors = SupervisorController.query_supervisors(query_dict={'group': [group]})
                            usernames = [supervisor.username for supervisor in supervisors]
                            query_dict.update(
                                {'meta.guider_group': [group], 'meta.guider_name':[usernames]})
                        else:
                            query_dict.update(
                                {'meta.guider_group': [group], 'meta.guider_name': [username]})
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func

