import json
import jieba
from collections import Counter
from app.core import dao
from app import redis_cli


class FormService:

    @classmethod
    def calculate_map(cls, meta_name):
        """
        督导的分布的计算, 包括对选项型的分布计算 和 文本型的并放入rediis
        :param meta_name:
        :return:
        """
        if meta_name is None:
            return
        item_map = {}
        word_cloud = {}
        forms, _ = dao.Form.query_forms(query_dict={"bind_meta_name": [meta_name], 'status': ['已完成']})

        for form in forms:
            for item in form.get("values", []):

                if item.get('item_type') == "radio_option":
                    # 处理单选
                    if not item_map.get(item['item_name']):
                        # 初始化
                        point = {o['value']: {"option": o, "num": 0} for o in item.get("payload", {}).get("options", [])}
                        if item.get('value'):
                            point[item['value']]['num'] = point[item['value']]['num'] + 1
                        item_map[item['item_name']] = {
                            "item_name": item['item_name'],
                            "point": list(point.values())
                        }
                    else:
                        # 存在直接+1
                        point = item_map[item['item_name']]["point"]
                        for p in point:
                            if p['option']['value'] == item['value']:
                                p['num'] = p['num'] + 1
                if item.get("item_type") == "checkbox_option":
                    # 处理多选
                    if not item_map.get(item['item_name']):
                        point = {o['label']: {"option": o, "num": 0} for o in item.get("payload", {}).get("options", [])}
                        if item["value"]:
                            for value in item["value"]:
                                if  value in point:
                                    point[value]["num"] = point[value]["num"] + 1
                            item_map[item['item_name']] = {
                                "item_name": item['item_name'],
                                "point": list(point.values())
                            }
                    else:
                        point = item_map[item['item_name']]["point"]
                        for p in point:
                            if p['option']['label'] in item['value']:
                                p['num'] = p['num'] + 1
                if item.get("item_type") == "raw_text":
                    # 处理文本分词
                    if not word_cloud.get(item['item_name']):
                        # 首次
                        value = item['value']
                        if value:
                            res = jieba.cut(value)
                            word_cloud[item['item_name']] = list(res)
                    else:
                        value = item['value']
                        if value:
                            if isinstance(value, str):
                                res = jieba.cut(value)
                            else:
                                res = jieba.cut(str(value))
                            word_cloud[item['item_name']] = word_cloud[item['item_name']] + list(res)

        # word_cloud 转成数组新式
        word_cloud = [{"item_name": k,
                       "value":
                           [
                               {"word": i[0],
                                "num": i[1]}
                               for i in Counter(v).items()]} for k, v in
                      word_cloud.items()
                      ]

        redis_cli.set("form_service:{}:word_cloud".format(meta_name), json.dumps(word_cloud))
        redis_cli.set("form_service:{}:map".format(meta_name), json.dumps(list(item_map.values())))
        print("计算完成")

    @classmethod
    def check_lesson_meta(cls, meta):
        """[检查meta的时间是否冲突, 一个督导一个时间只能有一门课]
        Arguments:
            meta {[type]} -- [description]
        """
        lesson_date = meta.get('lesson', {}).get('lesson_date')
        guider = meta.get('guider')
        lesson_times = meta.get('lesson', {}).get('lesson_times', [])

        forms, _ = dao.Form.query_forms(query_dict={
            'meta.lesson.lesson_date': lesson_date,
            'meta.guider': guider,
        })
        if forms:
            for form in forms:
                has_times = form.get('meta',{}).get('lesson', {}).get('lesson_times', []) 
                if set(has_times)  & set(lesson_times):
                    return False
        return True

