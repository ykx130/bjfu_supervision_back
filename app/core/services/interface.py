import json
import jieba
from collections import Counter
from app import redis_cli

class InterfaceService:

    @classmethod
    def update_page_data(cls):
        """
        更新首页数据
        :return:
        """
        #
        # (submitted_form_num, err) = get_submitted_form_num()
        # wait_submitted_form_num = get_wait_submitted_form_num()
        units = ['林学院', '水土保持学院', '生物科学与技术学院', '园林学院', '经济管理学院', '工学院',
                 '理学院', '信息学院', '人文社会科学学院', '外语学院', '材料科学与技术学院',
                 '自然保护区学院', '环境科学与工程学院', '艺术设计学院', '体育教学部', '马克思主义学院']
        for unit in units:
            pass
            # (unit_num, err) = find_form_unit_num(unit)
        #     redis_cli.set('sys:form_num:{unit}'.format(unit=unit), json.dumps(unit_num))
        # redis_cli.set("sys:submitted_form", json.dumps(submitted_form_num))
        # redis_cli.set("sys:wait_submitted_form", json.dumps(wait_submitted_form_num))
