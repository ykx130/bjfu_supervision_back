import json


def args_to_dict(condition):
    condition_fin = dict()
    for key in condition:
        for value in condition.getlist(key):
            try:
                value = json.loads(value)
            except:
                value = value
            if key not in condition_fin:
                condition_fin[key] = [value]
            else:
                condition_fin[key].append(value)
    if '_page' not in condition_fin:
        condition_fin['_page'] = [1]
    if '_per_page' not in condition_fin:
        condition_fin['_per_page'] = [100]
    return condition_fin
