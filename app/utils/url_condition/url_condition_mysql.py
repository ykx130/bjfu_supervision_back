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
        order_list = []
        sort_list = []
        for key, value in url_args.items():
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
                    is_equal = True  # 筛选是相等的标志
                    for item in filter_list:
                        if item in key and key.endswith(item):
                            is_equal = False
                            key = key[:len(key) - len(item)]
                            if key not in self.filter_dict:
                                self.filter_dict[key] = {item: v}
                            else:
                                self.filter_dict[key][item] = v
                            break
                    if is_equal:
                        if key not in self.filter_dict:
                            self.filter_dict[key] = {'_eq': [v]}
                        else:
                            self.filter_dict[key]['_eq'].append(v)
        if len(order_list) == len(sort_list):
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, order_list))
        else:
            self.sort_limit_dict['_sort_dict'] = dict(zip(sort_list, ['desc' for i in range(len(sort_list))]))


def filter_query(query, filter_map, name_map, base_table):
    for map_key, map_value in filter_map.items():
        params = map_key.split('.')
        column_name = params[len(params) - 1]
        if len(params) != 1:
            table_name = params[len(params) - 2]
            table = name_map[table_name]
        else:
            table = base_table
        for key, value in map_value.items():
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
                query = query.filter(getattr(table, column_name).in_(value))
            elif key == '_like':
                query = query.filter(getattr(table, column_name).like(value + '%'))
    return query


def sort_limit_query(query, sort_limit_dict, name_map):
    sort_dict = sort_limit_dict.get('_sort_dict', {})
    for sort_key, sort_value in sort_dict.items():
        params = sort_key.split('.')
        table_name = params[len(params) - 2]
        table = name_map[table_name]
        column_name = params[len(params) - 1]
        if sort_value == 'desc':
            query = query.order_by(getattr(table, column_name).desc())
        else:
            query = query.order_by(getattr(table, column_name))
    limit_num = sort_limit_dict.get('_limit', None)
    if limit_num is not None:
        query = query.limit(int(limit_num))
    return query


def page_query(query, page_dict):
    page = int(page_dict['_page']) if '_page' in page_dict else 1
    per_page = int(page_dict['_per_page']) if '_per_page' in page_dict else 20
    pagination = query.paginate(page=int(page), per_page=int(per_page), error_out=False)
    return pagination.items, pagination.total


def process_query(query, filter_dict, sort_limit_dict, page_dict, name_map, base_table):
    query = filter_query(query, filter_dict, name_map, base_table)
    query = sort_limit_query(query, sort_limit_dict, name_map)
    (query, total) = page_query(query, page_dict)
    return query, total


def count_query(query, filter_dict, sort_limit_dict, name_map, base_table):
    query = filter_query(query, filter_dict, name_map, base_table)
    query = sort_limit_query(query, sort_limit_dict, name_map)
    return query.count()
