import json


def init_filter_dict(filter_list):
    filter_dict = dict()
    for filter_item in filter_list:
        filter_dict[filter_item] = dict()
    return filter_dict


class UrlCondition(object):
    def __init__(self, url_args):
        filter_list = ['_lt', '_lte', '_gt', '_gte', '_ne', '_like', '_eq']
        self.filter_dict = dict()
        self.page_dict = {'_per_page': 20, '_page': 1}
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
                            if k not in self.filter_dict:
                                self.filter_dict[k] = {item: v}
                            else:
                                self.filter_dict[k][item] = v
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


def filter_query(query, filter_map, name_map):
    for map_key, map_value in filter_map:
        params = map_key.split('.')
        table_name = params[len(params) - 2]
        table = name_map[table_name]
        column_name = params[len(params) - 1]
        for key, value in map_value:
            if key == '_lt':
                query = query.filter(getattr(table, column_name) < value)
            elif key == '_lte':
                query = query.filter(getattr(table, column_name) <= value)
            elif key == '_ne':
                query = query.filter(getattr(table, column_name) != value)
            elif key == '_gt':
                query = query.filter(getattr(table, column_name) > value)
            elif key == '_gte':
                query = query.filter(getattr(table, column_name) >= value)
            elif key == '_eq':
                query = query.filter(getattr(table, column_name) == value)
            elif key == '_like':
                query = query.filter(getattr(table, column_name).like(value))
    return query


def sort_limit_dict(query, sort_limit_dict, name_map):
    for sort_key, sort_value in sort_limit_dict['_sort_dict']:
        params = sort_key.split('.')
        table_name = params[len(params) - 2]
        table = name_map[table_name]
        column_name = params[len(params) - 1]
        if sort_value == "desc":
            query = query.order_by(getattr(table, column_name).desc())
        else:
            query = query.order_by(getattr(table, column_name))
    limit_num = sort_limit_dict['_limit'] if '_limit' in sort_limit_dict else None
    if limit_num is not None:
        query.limit(int(limit_num))
    return query


def process_query(query, url_condition, name_map):
    query = filter_query(query, url_condition.filter_dict, name_map)
