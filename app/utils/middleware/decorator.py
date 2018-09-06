func_map = dict()


def mapper(name):
    def decorator(func):
        if name not in func_map:
            func_map[name] = [func]
        else:
            func_map[name].append(func)
        return func

    return decorator
