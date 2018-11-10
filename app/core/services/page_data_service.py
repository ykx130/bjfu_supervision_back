from app import redis_cli
from app.core.services import supervisor_service, form_service, notice_lesson_service
import json

def get_page_data_service():
    data_dict = dict()
    data_func = {"sys:guider_num": supervisor_service.get_supervisor_num,
                 "sys:submitted_form": form_service.get_submitted_form_num,
                 "sys:wait_submitted_form": form_service.get_wait_submitted_form_num,
                 "sys:notice_lesson_num": notice_lesson_service.get_notice_lesson_num
                 }
    units = ['林学院', '水土保持学院', '生物科学与技术学院', '园林学院', '经济管理学院', '工学院',
             '理学院', '信息学院', '人文社会科学学院', '外语学院', '材料科学与技术学院',
             '自然保护区学院', '环境科学与工程学院', '艺术设计学院', '体育教学部', '马克思主义学院']
    data_dict['sys:form_num'] = dict()
    for unit in units:
        find_name = 'sys:form_num:{unit}'.format(unit=unit)
        if redis_cli.exists(find_name):
            data_dict['sys:form_num'][unit] = json.loads(redis_cli.get(find_name))
        else:
            (data, err) = form_service.find_form_unit_num(unit)
            if err is not None:
                return None, err
            data_dict['sys:form_num'][unit] = data
            redis_cli.set(find_name, json.dumps(data))
    for data_name, func in data_func.items():
        if redis_cli.exists(data_name):
            data_dict[data_name] = json.loads(redis_cli.get(data_name))
        else:
            (data, err) = func()
            if err is not None:
                return None, err
            data_dict[data_name] = data
            redis_cli.set(data_name, json.dumps(data))
    return data_dict, None
