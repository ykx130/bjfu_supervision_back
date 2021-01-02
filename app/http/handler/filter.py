from functools import wraps
from app.core.controller.user import AuthController, SupervisorController
from app.core.services.term import TermService
from flask import jsonify, request, g
from app.utils import args_to_dict

UserRoleMap = {
    'admin': "管理员",
    "grouper": "小组长",
    "main_grouper": "大组长",
    "leader": "学院领导",
    "guider": "督导",
    "teacher": "教师",
    'reader':"校级管理员",
    'develop_admin':'教发管理员'
}


class Filter(object):

    @classmethod
    def fiilter_leader_unit_permission(cls):
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

                    supervisor_role_names = ['督导', '小组长', '大组长']

                    current_role = UserRoleMap.get(request.headers.get('CurrentRole', None), '教师')
                    if current_role is None or current_role not in role_names:
                        return jsonify({
                            'code': 403,
                            'msg': 'forbidden'
                        }), 403

                    
                    if current_role == '学院领导':
                        query_dict.update({'unit': [user['unit']]})
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func


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
                    term = query_dict.get('term')
                    supervisor_role_names = ['督导', '小组长', '大组长']

                    current_role = UserRoleMap.get(request.headers.get('CurrentRole', None), '教师')
                    if current_role is None or current_role not in role_names:
                        return jsonify({
                            'code': 403,
                            'msg': 'forbidden'
                        }), 403

                    if current_role == '管理员' or current_role == '校级管理员' or current_role=='教发管理员':
                        query_dict = query_dict
                    elif current_role == '学院领导':
                        query_dict.update({'unit': [user['unit']]})
                    elif current_role in supervisor_role_names:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group_name')
                        if current_role == '大组长':
                            query_dict = query_dict
                        elif current_role == '小组长':
                            supervisors, _ = SupervisorController.query_supervisors(
                                query_dict={'group_name': [group]})
                            usernames = [supervisor.get('username') for supervisor in supervisors]
                            query_dict.update(
                                {'group_name': [group], 'username': usernames})
                        else:
                            query_dict.update(
                                {'group_name': [group], 'username': [username], 'user_id': [user_id]})
                    else:
                        query_dict.update({'username': [username], 'user_id': [user_id]})
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
                    supervisor_role_names = ['督导', '小组长', '大组长']
                    term = query_dict.get('meta.term')
                    if term is None:
                        term = TermService.get_now_term()['name']
                    current_role = UserRoleMap.get(request.headers.get('CurrentRole', None), '教师')
                    if current_role is None or current_role not in role_names:
                        return jsonify({
                            'code': 403,
                            'msg': 'forbidden'
                        }), 403

                    if current_role == '管理员' or  current_role == '校级管理员' or current_role=='教发管理员':                       
                        query_dict = query_dict
                    elif current_role == '学院领导':
                        query_dict.update({'meta.lesson.lesson_teacher_unit': user.get('unit')})
                    elif current_role in supervisor_role_names:
                        current_supervisor = SupervisorController.get_supervisor_by_username(
                            query_dict={'username': username})
                        group = current_supervisor.get('group_name')
                        if current_role == '大组长':
                            query_dict = query_dict
                        elif current_role == '小组长':
                            supervisors, _ = SupervisorController.query_supervisors(query_dict={'group_name': [group]})
                            usernames = [supervisor.get('username') for supervisor in supervisors]
                            query_dict.update(
                                {'meta.guider_group': group, 'meta.guider': usernames})
                        else:
                            query_dict.update(
                                {'meta.guider_group': group, 'meta.guider': username})
                print(query_dict)
                result = func(*args, **query_dict)
                return result

            return wrapper

        return filter_func
