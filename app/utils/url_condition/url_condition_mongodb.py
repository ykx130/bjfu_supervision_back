'''
@Author: your name
@Date: 2019-11-23 18:09:17
@LastEditTime: 2019-11-23 18:09:33
@LastEditors: Please set LastEditors
@Description: In User Settings Edi
@FilePath: /bjfu_supervision_back/app/utils/url_condition/url_condition_mongodb.py
'''
import json
from flask_pymongo import ObjectId


def object_to_str(dict_unserializalbe):
    for k, v in dict_unserializalbe.items():
        if type(v) == ObjectId:
            dict_unserializalbe[k] = str(v)
    return dict_unserializalbe


def dict_serializable(dict_unserializalbe):
    r = dict()
    for k, v in dict_unserializalbe.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = str(v)
    return r


class UrlCondition(object):
    def __init__(self, url_args):
        if url_args is None:
            url_args = dict()
        self.sort_limit_dict = dict()
        self.page_dict = dict()
        self.filter_dict = dict()
        order_list = []
        sort_list = []
        filter_list = ['_lt', '_lte', '_gt', '_gte', '_ne','_like']
        for key, value in url_args.items():
            if type(value) is not list:
                value = [value]
            for v in value:
                if key == '_per_page' or key == '_page':
                    self.page_dict[key] = v
                elif key == '_sort':
                    v = v.replace(' ', '')
                    sort_list = v.split(',')
                elif key == '_order':
                    v = v.replace(' ', '')
                    order_list = [int(item_order) for item_order in v.split(',')]
                elif key == '_limit':
                    self.sort_limit_dict[key] = v
                else:
                    isEqual = True  # 筛选是相等的标志
                    for item in filter_list:
                        if item in key and key.endswith(item):
                            isEqual = False
                            if item == '_like':
                                self.filter_dict[key[:len(key) - len('_like')]] = {'$regex': v}
                            else:
                                key = key[:len(key) - len(item)]
                                self.filter_dict[key] = {'${}'.format(item[1:]): v}
                            break
                    if isEqual:
                        if key not in self.filter_dict:
                            self.filter_dict[key] = {'$in': [v]}
                        else:
                            self.filter_dict[key]['$in'].append(v)
        if len(order_list) == len(sort_list):
            self.sort_limit_dict['_sort_dict'] = [(order_list[i], sort_list[i]) for i in range(len(sort_list))]
        elif len(order_list) == 0:
            self.sort_limit_dict['_sort_dict'] = [(sort_list[i], 1) for i in range(len(sort_list))]


# 将请求的url_args分解成三个字典
# sort_limit_dict 用于排序和限制数量
# page_dict 用于分页
# filter_dict 用于筛选数据


class Paginate(object):
    def __init__(self, _data, page_dict):
        self.per_page = page_dict.get('_per_page', 1000000)
        self.page = page_dict.get('_page', 1)
        self.total = _data.count()
        self.page_num = self.total // self.per_page + 1 if self.total % self.per_page != 0 else self.total // self.per_page
        self.prev = self.page - 1 if self.page > 1 else None
        self.next = self.page + 1 if self.page < self.page_num else None
        self.has_prev = True if self.page > 1 else False
        self.has_next = True if self.page < self.page_num else False
        self.data_page = _data.limit(self.per_page).skip((self.page - 1) * self.per_page)


def sort_limit(datas, sort_limit_dict):
    dataspage = datas
    _limit = sort_limit_dict.get('_limit', None)
    _sort_dict = sort_limit_dict.get('_sort_dict', [])
    if _limit is not None:
        dataspage = dataspage.limit(_limit)
    if len(_sort_dict) > 0:
        print(_sort_dict)
        dataspage = dataspage.sort(_sort_dict)
    return dataspage
