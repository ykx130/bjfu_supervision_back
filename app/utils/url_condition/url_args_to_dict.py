def args_to_dict(condition):
    condition_fin = dict()
    for key in condition:
        for value in condition.getlist(key):
            if key not in condition_fin:
                condition_fin[key] = [value]
            else:
                condition_fin[key].append(value)
    return condition_fin
