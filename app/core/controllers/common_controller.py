import json
from flask_pymongo import ObjectId

def object_to_str(dict_unserializalbe):
    for k, v in dict_unserializalbe.items():
        if type(v) == ObjectId:
            dict_unserializalbe[k] = str(v)
    return dict_unserializalbe

def dict_serializable(dict_unserializalbe):
    r = {}
    for k, v in dict_unserializalbe.items():
        try:
            r[k] = json.loads(v)
        except:
            r[k] = str(v)
    return r


class UrlCondition(object):
    def __init__(self, url_args):
        self.sort_limit_dict = {}
        self.page_dict = {}
        self.filter_dict = {}
        order_list = []
        sort_list = []
        filter_list = ['_lt', '_lte', '_gt', '_gte', '_ne']
        for k in url_args:
            for v in url_args.getlist(k):
                try:
                    v = json.loads(v)
                except:
                    v = v
                if k == '_per_page' or k == '_page':
                    self.page_dict[k] = v
                elif k == '_sort':
                    v = v.replace(' ','')
                    sort_list = v.split(',')
                elif k == '_order':
                    v = v.replace(' ','')
                    order_list = [int(item_order) for item_order in v.split(',')]
                elif k == '_limit':
                    self.sort_limit_dict[k] = v
                else:
                    isEqual = True #筛选是相等的标志
                    for item in filter_list:
                        if item in k and k.endswith(item):
                            isEqual = False
                            k = k[:len(k)-len(item)]
                            self.filter_dict[k] = {'${}'.format(item[1:]):v}
                            break
                    if isEqual:
                        if k not in self.filter_dict:
                            self.filter_dict[k]={'$in':[v]}
                        else:
                            self.filter_dict[k]['$in'].append(v)
        if len(order_list) == len(sort_list):
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, order_list))
        elif len(order_list) == 0:
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, [1 for i in range(len(sort_list))]))

#将请求的url_args分解成三个字典
#sort_limit_dict 用于排序和限制数量
#page_dict 用于分页
#filter_dict 用于筛选数据


class Paginate(object):
    def __init__(self, _data, page_dict):
        self.per_page = page_dict.get('_per_page', None)
        self.page = page_dict.get('_page', None)
        if self.per_page is None:
            self.per_page = 20
        if self.page is None:
            self.page = 1
        self.total = _data.count()
        self.page_num = self.total // self.per_page + 1 if self.total % self.per_page != 0 else self.total // self.per_page
        self.prev = self.page - 1 if self.page > 1 else None
        self.next = self.page + 1 if self.page < self.page_num else None
        self.has_prev = True if self.page > 1 else False
        self.has_next = True if self.page < self.page_num else False
        self.data_page = _data.limit(self.per_page).skip((self.page-1)*self.per_page)



def sort_limit(datas, sort_limit_dict):
    dataspage = datas
    _limit = sort_limit_dict.get('_limit', None)
    _sort_dict = sort_limit_dict.get('_sort_dict', {})
    if _limit is not None:
        dataspage = dataspage.limit(_limit)
    if _sort_dict != {}:
        dataspage = dataspage.sort(_sort_dict)
    return dataspage

