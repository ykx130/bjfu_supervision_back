import json


def init_filter_dict(filter_list):
    filter_dict = dict()
    for filter_item in filter_list:
        filter_dict[filter_item] = dict()
    return filter_dict

class UrlCondition(object):
    def __init__(self, url_args):
        filter_list = ['_lt', '_lte', '_gt', '_gte', '_ne', '_like', '_eq']
        self.filter_dict = init_filter_dict()
        self.page_dict = dict()
        self.blur_dict = dict()
        self.sort_limit_dict = dict()
        for k in url_args:
            for v in url_args.getlist(k):
                try:
                    v = json.loads(v)
                except:
                    v = v
                if k == '_per_page' or k == '_page':
                    self.page_dict[k] = v
                elif k == '_sort':
                    v = v.replace(' ', '')
                    sort_list = v.split(',')
                elif k == '_order':
                    v = v.replace(' ', '')
                    order_list = [int(item_order) for item_order in v.split(',')]
                elif k == '_limit':
                    self.sort_limit_dict[k] = v
                else:
                    is_equal = True  # 筛选是相等的标志
                    for item in filter_list:
                        if item in k and k.endswith(item):
                            is_equal = False
                            k = k[:len(k) - len(item)]
                            self.filter_dict[item][k] = v
                            break
                    if is_equal:
                        if k not in self.filter_dict:
                            self.filter_dict[k] = [v]
                        else:
                            self.filter_dict[k].append(v)
                if len(order_list) == len(sort_list):
                    self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, order_list))
                else:
                    self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, ["desc" for i in range(len(sort_list))]))


