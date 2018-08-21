from app.core.models.user_event import User, Event
from flask_pymongo import ObjectId


def find_users(mongo, condition=None):
    if condition is None:
        condition['using'] = True
        return mongo.db.user.find(condition), None
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    try:
        datas = mongo.db.user.find(condition)
    except Exception as e:
        return None, e
    return datas, None


def find_user(mongo, _id):
    try:
        condition = {'using': True, '_id': ObjectId(_id)}
        datas = mongo.db.user.find_one(condition)
    except Exception as e:
        return None, e
    return datas, None


def insert_user(mongo, user):
    user.items_to_dict()
    try:
        mongo.db.user.insert(user.model)
    except Exception as e:
        return False, e
    return True, None


def delete_user(mongo, condition=None):
    if condition is None:
        return False, None
    try:
        mongo.db.user.update(condition, {"$set": {"using": False}})
    except Exception as e:
        return False, e
    return True, None


def request_to_class(json_request):
    user = User()
    name = json_request.get('name', None)
    information_datas = json_request.get('information', {})
    events_datas = json_request.get('events', [])
    user.name = name
    if information_datas is not None:
        for k, v in information_datas.items():
            user.model['information'][k] = v
    if events_datas is not None:
        for events_data in events_datas:
            event = Event()
            for k, v in events_data.items():
                event.model[k] = v
            user.events.append(event)
    return user


def update_user(mongo, condition=None, change_items=None):
    if condition is None:
        condition = dict()
        condition['using'] = True
    try:
        mongo.db.user.update(condition, {"$set": change_items})
    except Exception as e:
        return False, e
    return True, None


def to_json_list(user):
    _id = user.get('_id', None)
    name = user.get('name', None)
    information = user.get('information', {})
    events = user.get('events', [])
    json_list = {
        '_id': _id,
        'name ': name,
        'information': information,
        'events': events
    }
    return json_list


def request_to_class_event(json_request):
    event = Event()
    event_id = json_request.get('event_id', None)
    time = json_request.get('time', None)
    value = json_request.get('value', None)
    discripe = json_request.get('discripe', None)
    event.event_id = event_id
    event.time = time
    event.value = value
    event.discripe = discripe
    return event


def number_event(events):
    for id, data in enumerate(events):
        try:
            data["event_id"] = id
        except:
            pass


def insert_event(json_request, mongo, _id):
    condition = {'using': True, '_id': ObjectId(_id)}
    event = request_to_class_event(json_request)
    try:
        user_datas = mongo.db.user.find_one(condition)
    except Exception as e:
        return False, e
    user_datas["events"].append(event.model)
    number_event(user_datas["events"])
    try:
        mongo.db.user.update(condition, {"$set": {"events": user_datas["events"]}})
    except Exception as e:
        return False, e
    return True, None


def find_event(mongo, _id, event_id):
    condition_user = {'using': True, '_id': ObjectId(_id)}
    try:
        user_data = mongo.db.user.find_one(condition_user)
    except Exception as e:
        return None, e
    if user_data is None:
        return None, None
    for event_data in user_data["events"]:
        if event_data["event_id"] == event_id:
            return event_data, None
    return None, None


def delete_event(mongo, _id, event_id):
    condition_user = {'using': True, '_id': ObjectId(_id)}
    user_data = mongo.db.user.find_one(condition_user)
    if user_data is None:
        return False, None
    for event_data in user_data["events"]:
        if event_data["event_id"] == event_id:
            event_data["event_using"] = False
            break
    try:
        mongo.db.user.update(condition_user, {"$set": {"events": user_data["events"]}})
    except Exception as e:
        return False, e
    return True, None


def update_event(mongo, _id, event_id, json_request):
    event = request_to_class_event(json_request)
    condition_user = {'using': True, '_id': ObjectId(_id)}
    try:
        user_data = mongo.db.user.find_one(condition_user)
    except Exception as e:
        return False, e
    if user_data is None:
        return False, None
    for event_data in user_data["events"]:
        if event_data["event_id"] == event_id:
            user_data["events"].remove(event_data)
            break
    user_data["events"].append(event.model)
    number_event(user_data["events"])
    try:
        mongo.db.user.update(condition_user, {"$set": {"events": user_data["events"]}})
    except Exception as e:
        return False, e
    return True, None
