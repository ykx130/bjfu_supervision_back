import json


class UrlCondition(object):
    def __init__(self, url_args):
        filter_list = ['_lt', '_lte', '_gt', '_gte', '_ne', '_like', '_eq']
        self.filter_dict = self.init_filter_dict(filter_list)
        self.page_dict = dict()
        self.sort_limit_dict = dict()
        order_list = []
        sort_list = []
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
                    order_list = [str(item_order) for item_order in v.split(',')]
                elif key == '_limit':
                    self.sort_limit_dict[key] = v
                else:
                    is_equal = True
                    for item in filter_list:
                        if item in key and key.endswith(item):
                            key = key[:len(key) - len(item)]
                            if item != '_eq':
                                is_equal = False
                                self.filter_dict[item][key] = v
                            break
                    if is_equal:
                        if key in self.filter_dict['_eq']:
                            self.filter_dict['_eq'][key].append(v)
                        else:
                            self.filter_dict['_eq'][key] = [v]
        if len(order_list) == len(sort_list):
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, order_list))
        else:
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, ['desc' for i in range(len(sort_list))]))

    @classmethod
    def init_filter_dict(cls, filter_list):
        filter_dict = dict()
        for filter_item in filter_list:
            filter_dict[filter_item] = dict()
        return filter_dict


def filter_query(query, filter_map, table):
    for map_key, map_value in filter_map.items():
        for key, value in map_value.items():
            if hasattr(table, key):
                if map_key == '_lt':
                    query = query.filter(getattr(table, key) < value)
                elif map_key == '_lte':
                    query = query.filter(getattr(table, key) <= value)
                elif map_key == '_ne':
                    query = query.filter(getattr(table, key) != value)
                elif map_key == '_gt':
                    query = query.filter(getattr(table, key) > value)
                elif map_key == '_gte':
                    query = query.filter(getattr(table, key) >= value)
                elif map_key == '_eq':
                    query = query.filter(getattr(table, key).in_(value))
                elif map_key == '_like':
                    query = query.filter(getattr(table, key).like(value + '%'))
    return query


def sort_limit_query(query, sort_limit_dict, table):
    sort_dict = sort_limit_dict.get('_sort_dict', {})
    for sort_key, sort_value in sort_dict.items():
        if sort_value == 'desc':
            query = query.order_by(getattr(table, sort_key).desc())
        else:
            query = query.order_by(getattr(table, sort_key))
    limit_num = sort_limit_dict.get('_limit', None)
    if limit_num is not None:
        query = query.limit(int(limit_num))
    return query


def page_query(query, page_dict):
    if '_page' not in page_dict or '_per_page' not in page_dict:
        data = query.all()
        return data, len(data)
    page = int(page_dict['_page'])
    per_page = int(page_dict['_per_page'])
    pagination = query.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total


def process_query(query, filter_dict, sort_limit_dict, table):
    query = filter_query(query, filter_dict, table)
    query = sort_limit_query(query, sort_limit_dict, table)
    return query


def count_query(query, filter_dict, sort_limit_dict, table):
    query = filter_query(query, filter_dict, table)
    query = sort_limit_query(query, sort_limit_dict, table)
    return query.count()
