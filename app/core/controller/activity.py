import app.core.dao as dao
from app.utils import CustomError, db
from app.utils.kafka import send_kafka_message
from datetime import datetime
from flask_login import current_user
import app.core.services as service
import pandas

class ActivityController(object):
    @classmethod
    def formatter(cls, activity: dict):
        return activity

    @classmethod
    def reformatter(cls, data: dict):
        new_data = dict()
        must_column = 'start_time'
        if must_column not in data:
            raise CustomError(200, 500, must_column + ' not found')
        for key, value in data.items():
            if key not in ['apply_state', 'attend_num', 'remainder_num']:
                new_data[key] = value
        start_time = data.get('start_time', None)
        now = datetime.now()
        if str(now) > start_time:
            new_data['apply_state'] = '活动已结束'
        else:
            new_data['apply_state'] = '报名进行中'
        if 'attend_num' not in data:
            new_data['attend_num'] = 0
            new_data['remainder_num'] = data['all_num']
        else:
            new_data['attend_num'] = data['attend_num']
            new_data['remainder_num'] = data['all_num']-data['attend_num']
        return new_data

    @classmethod
    def reformatter_query(cls, data: dict):
        return data

    @classmethod
    def insert_activity(cls, ctx: bool = True, data: dict = None):
        if data is None:
            data = {}
        term = data.get('term', service.TermService.get_now_term()['name'])
        data['term'] = term
        (_, num) = dao.Activity.query_activities(query_dict={'title': [data.get('title', '')]}, unscoped=False)
        if num != 0:
            raise CustomError(500, 200, 'title has been used')
        data = cls.reformatter(data)
        try:
            dao.Activity.insert_activity(ctx=False, data=data)
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
    def import_activity_excel(cls, ctx: bool = True, data=None):
        if 'filename' in data.files:
            from app import basedir
            filename = basedir + '/static/' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            file = data.files['filename']
            file.save(filename)
            df = pandas.read_excel(filename)
        else:
            raise CustomError(500, 200, 'file must be given')
        column_dict = {'题目': 'title', '主讲人': 'presenter', '学期': 'term',
                       '所属模块': 'module', '开始时间': 'start_time', '地点': 'place',
                       '主办单位': 'organizer','学时':'period','允许报名人数':'all_num','是否为新教师必修':'is_obligatory'}
        row_num = df.shape[0]
        fail_activities = list()
        try:
            for i in range(0, row_num):
                activity_dict = dict()
                for col_name_c, col_name_e in column_dict.items():
                    activity_dict[col_name_e] = str(df.iloc[i].get(col_name_c, ''))
                activity_dict['apply_state'] = '可报名'
                (_, num) = dao.Activity.query_activities(query_dict={
                    'title': activity_dict['title'] ,
                    'term': activity_dict['term']
                }, unscoped=False)
                if num != 0:
                    fail_activities.append({**activity_dict, 'reason': '活动已经存在'})
                    continue
                dao.Activity.insert_activity(ctx=True, data=activity_dict)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            raise e
        file_path = None
        if len(fail_activities) != 0:
            frame_dict = {}
            for fail_activity in fail_activities:
                for key, value in column_dict.items():
                    if value in fail_activity:
                        excel_value = fail_activity.get(value)
                        if key not in frame_dict:
                            frame_dict[key] = [excel_value]
                        else:
                            frame_dict[key].append(excel_value)
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + "fail" + \
                       datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123',
                           index=False, header=True)
        return file_path

    @classmethod
    def update_activity(cls, ctx: bool = True, id: int = 0, data: dict = None):
        if data is None:
            data = {}
        activity = dao.Activity.get_activity(query_dict={'id':id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        data = cls.reformatter(data)
        try:
            dao.Activity.update_activity(ctx=False, query_dict={'id': [id]}, data=data)
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
    def delete_activity(cls, ctx: bool = True, id: int = 0):
        activity = dao.Activity.get_activity(query_dict={'id':id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        try:
            dao.Activity.delete_activity(ctx=False, query_dict={'id': [id]})
            dao.ActivityUser.delete_activity_user(ctx=False, query_dict={'activity_id': [id]})
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
    def get_activity(cls, query_dict, unscoped: bool = False):
        activity = dao.Activity.get_activity(query_dict=query_dict, unscoped=unscoped)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        return cls.formatter(activity)

    @classmethod
    def query_activities(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        (activities, num) = dao.Activity.query_activities(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(activity) for activity in activities], num


class ActivityUserController(object):
    @classmethod
    def formatter(cls, activity_user):
        user = dao.User.get_user(query_dict={'username':activity_user['username']}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        activity_user_dict = {
            'user': user,
            'state': activity_user['state'],
            'fin_state': activity_user['fin_state']
        }
        return activity_user_dict

    @classmethod
    def reformatter(cls, data):
        if 'fin_state' not in data:
            raise CustomError(500, 200, 'fin_state must be given')
        if 'state' not in data:
            data['state'] = '已报名'
        return data

    @classmethod
    def query_activity_users(cls, query_dict: dict = None, unscoped: bool = False):
        if query_dict is None:
            query_dict = {}
        (activity_users, num) = dao.ActivityUser.query_activity_users(query_dict=query_dict, unscoped=unscoped)
        return [cls.formatter(activity_user) for activity_user in activity_users], num

    @classmethod
    def get_activity_user(cls, query_dict, unscoped: bool = False):
        activity_user = dao.ActivityUser.get_activity_user(query_dict=query_dict, unscoped=unscoped)
        if activity_user is None:
            raise CustomError(404, 404, 'activity_user not found')
        return cls.formatter(activity_user)

    @classmethod
    def insert_activity_user(cls, ctx: bool = True, activity_id: int = 0, data: dict = None):
        if data is None:
            data = {}
        activity = dao.Activity.get_activity(query_dict={'id': activity_id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        username = data.get('username', current_user.username)
        user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        if activity['apply_state'] =='活动已结束':
            raise CustomError(500, 200, activity['apply_state'])
        if activity['remainder_num'] <= 0:
            raise CustomError(500, 200, 'remain number is zero')
        data['activity_id'] = activity_id
        data['username'] = username
        data['activity_type']='培训'
        data = cls.reformatter(data)
        remainder_num = activity['remainder_num'] - 1
        attend_num = activity['attend_num'] + 1
        (_, num) = dao.ActivityUser.query_activity_users(
            query_dict={'activity_id': [activity_id], 'username': [username]}, unscoped=False)
        if num > 0:
            raise CustomError(500, 200, 'activity_user has existed')
        try:
            dao.Activity.update_activity(ctx=False, query_dict={'id': [activity_id]},
                                         data={'remainder_num': remainder_num, 'attend_num': attend_num})
            dao.ActivityUser.insert_activity_user(ctx=False, data=data)
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
    def insert_activity_user_apply(cls, ctx: bool = True, username: str = None, data: dict = None):
        if data is None:
            data = {}
        term = data.get('term', service.TermService.get_now_term()['name'])
        data['term'] = term
        (_, num) = dao.Activity.query_activities(query_dict={'title': [data.get('title', '')]}, unscoped=False)
        if num != 0:
            raise CustomError(500, 200, 'title has been used')
        data['apply_state'] ='待审核活动'
        try:
            dao.Activity.insert_activity(ctx=False, data=data)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            if isinstance(e, CustomError):
                raise e
            else:
                raise CustomError(500, 500, str(e))
        activity = dao.Activity.get_activity(query_dict={'title':  [data.get('title', '')],'term': [data.get('term', '')]}, unscoped=False)
        activity_user_dict={}
        activity_user_dict['activity_id']=activity['activity_id']
        if username is None:
            username=current_user.username
        user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        activity_user_dict['username'] = username
        activity_user_dict['activity_type'] = '培训'
        activity_user_dict['state']='已报名'
        activity_user_dict['fin_state']=data['fin_state']
        (_, num) = dao.ActivityUser.query_activity_users(
            query_dict={'activity_id': [activity['activity_id']], 'username': [username]}, unscoped=False)
        if num > 0:
            raise CustomError(500, 200, 'activity_user has existed')
        try:
            dao.ActivityUser.insert_activity_user(ctx=False, data=activity_user_dict)
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
    def import_activity_user_excel(cls, ctx: bool = True,activity_id: int = 0, data=None):
        if 'filename' in data.files:
            from app import basedir
            filename = basedir + '/static/' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            file = data.files['filename']
            file.save(filename)
            df = pandas.read_excel(filename)
        else:
            raise CustomError(500, 200, 'file must be given')
        fail_activity_users = list()
        activity = dao.Activity.get_activity(query_dict={'id': activity_id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        column_dict = {'教师工号': 'username', '参与状态': 'fin_state'}
        row_num = df.shape[0]
        try:
            for i in range(0, row_num):
                activity_user_dict = dict()
                activity_user_dict['activity_id']=activity_id
                for col_name_c, col_name_e in column_dict.items():
                    activity_user_dict[col_name_e] = str(df.iloc[i].get(col_name_c, ''))
                activity_user_dict['state']='已报名'
                activity_user_dict['activity_type'] ='培训'
                username = activity_user_dict['username']
                user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
                if user is None:
                    fail_activity_users.append({**activity_user_dict, 'reason': '用户不存在'})
                    continue
                (_, num) = dao.ActivityUser.query_activity_users(query_dict={
                    'username': activity_user_dict['username'],
                    'activity_id': activity_user_dict['activity_id']
                }, unscoped=False)
                if num != 0:
                    dao.ActivityUser.update_activity_user(ctx=False,
                                                  query_dict={'activity_id': [activity_id], 'username': [username]},
                                                  data=activity_user_dict)
                    continue
                dao.Activity.insert_activity(ctx=True, data=activity_user_dict)
            if ctx:
                db.session.commit()
        except Exception as e:
            if ctx:
                db.session.rollback()
            raise e
        file_path = None
        if len(fail_activity_users) != 0:
            frame_dict = {}
            for fail_activity_user in fail_activity_users:
                for key, value in column_dict.items():
                    if value in fail_activity_user:
                        excel_value = fail_activity_user.get(value)
                        if key not in frame_dict:
                            frame_dict[key] = [excel_value]
                        else:
                            frame_dict[key].append(excel_value)
            frame = pandas.DataFrame(frame_dict)
            from app import basedir
            filename = '/static/' + "fail" + \
                       datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx'
            fullname = basedir + filename
            frame.to_excel(fullname, sheet_name='123',
                           index=False, header=True)
        return file_path

    @classmethod
    def update_activity_user(cls, ctx: bool = True, activity_id: int = 0, username: str = None, data: dict = None):
        if data is None:
            data = {}
        user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        activity = dao.Activity.get_activity(query_dict={'id': activity_id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        activity_user = dao.ActivityUser.get_activity_user(
            query_dict={'activity_id': activity_id, 'username': username}, unscoped=False)
        if activity_user is None:
            raise CustomError(404, 404, 'activity_user not found')
        new_data = dict()
        for key, value in data.items():
            if key not in ['username', 'activity_id', 'username']:
                new_data[key] = value
        try:
            dao.ActivityUser.update_activity_user(ctx=False,
                                                  query_dict={'activity_id': [activity_id], 'username': [username]},
                                                  data=new_data)
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
    def delete_activity_user(cls, ctx: bool = True, activity_id: int = 0, username: str = None):
        user = dao.User.get_user(query_dict={'username': username}, unscoped=False)
        if user is None:
            raise CustomError(404, 404, 'user not found')
        activity = dao.Activity.get_activity(query_dict={'id': activity_id}, unscoped=False)
        if activity is None:
            raise CustomError(404, 404, 'activity not found')
        activity_user = dao.ActivityUser.get_activity_user(
            query_dict={'activity_id': activity_id, 'username': username}, unscoped=False)
        if activity_user is None:
            raise CustomError(404, 404, 'activity_user not found')
        attend_num = activity['attend_num'] - 1
        remainder_num = activity_id['remainder_num'] + 1
        try:
            dao.ActivityUser.delete_activity_user(ctx=False, query_dict={'id': [activity_user['id']]})
            dao.Activity.update_activity(ctx=False, query_dict={'id': [activity_id]},
                                         data={'attend_num': attend_num, 'remainder_num': remainder_num})
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
    def query_current_user_activities(cls, username: str, query_dict: dict = None):
        if query_dict is None:
            query_dict = {}
        state = query_dict.get('state', [])
        if len(state) > 0:
            state = state[0]

        current_user_activities = list()

        if state == 'hasAttended':
            (activity_users, _) = dao.ActivityUser.query_activity_users(
                query_dict={'username': [username], 'state_ne': ['未报名']}, unscoped=False)
            for activity_user in activity_users:
                activity = dao.Activity.get_activity(query_dict={'id':activity_user['activity_id']}, unscoped=False)
                if activity is None:
                    raise CustomError(404, 404, 'activity not found')
                current_user_activity = {
                    'activity': activity,
                    'activity_user': {
                        'state': activity_user['state'],
                        'fin_state': activity_user['fin_state']
                    }
                }
                current_user_activities.append(current_user_activity)
            return current_user_activities, len(current_user_activities)

        elif state == 'canAttend':
            (has_attend_activity_users, _) = dao.ActivityUser.query_activity_users(
                query_dict={'username': [username], 'state_ne': ['未报名']}, unscoped=False)
            has_attend_activity_ids = [has_attend_activity_user['activity_id'] for has_attend_activity_user in
                                       has_attend_activity_users]
            (all_can_attend_activities, _) = dao.Activity.query_activities(
                query_dict={'apply_state': ['报名进行中'], 'remainder_num_gte': [0], 'id_ne': has_attend_activity_ids})
            for activity in all_can_attend_activities:
                current_user_activity = {
                    'activity': activity,
                    'activity_user': {
                        'state': '未报名',
                        'fin_state': '未参加'
                    }
                }
                current_user_activities.append(current_user_activity)
            return current_user_activities, len(current_user_activities)
        else:
            raise CustomError(500, 200, 'state is wrong')
