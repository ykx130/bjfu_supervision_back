import app.core.dao as dao


class UserController():
    @classmethod
    def role_list(cls, user: dict, term: str):
        term_name = term.get('name', None)
        role_list = {'is_grouper': '小组长', 'is_main_grouper': '大组长', 'is_admin': '管理员', 'is_leader': '领导',
                     'is_guider': '督导'}
        role_names = ['教师']
        for role_name_e, role_name_c in role_list.items():
            if user[role_name_e] is True:
                role_names.append(role_name_c)
        if user['is_guider']:
            (supervisor, err) = dao.Supervisor.get_supervisor(user['username'], term_name)
            if err is None:
                return None, err
            for role_name_e, role_name_c in role_list.items():
                if supervisor[role_name_e] is True:
                    role_names.append(role_name_c)
        return role_names, None

    @classmethod
    def formatter(cls, user: dict):
        (term, err) = dao.Term.get_now_term()
        if err is not None:
            return list(), err
        (role_names, err) = cls.role_list(user)
        if err is not None:
            return None, err
        user['role_names'] = role_names
        if user['is_guider']:
            (supervisor, err) = dao.Supervisor.get_supervisor(user['username'], term)
            if err is not None:
                return None, err
            user['guider'] = supervisor
        return user, None

    @classmethod
    def query_users(cls, query_dict: dict = None):
        (users, num, err) = dao.User.query_users(query_dict)
        if err is not None:
            return None, None, err
        return [cls.formatter(user) for user in users], num, None


