from app.core.models import User,Event
from flask_pymongo import ObjectId

def find_users(mongo,condition=None):
    condition['using']=True
    if condition is None:
        return mongo.db.user.find()
    if '_id' in condition:
        condition['_id']['$in']=[ObjectId(item) for item in condition['_id']['$in']]
    datas=mongo.db.user.find(condition)
    return datas

def find_user(mongo, _id):
    try:
        condition={'using':True,'_id':ObjectId(_id)}
    except:
        return None
    datas = mongo.db.user.find(condition)
    return datas


def insert_user(mongo, user):
    user.items_to_dict()
    mongo.db.user.insert(user.model)


def delete_user(mongo, condition=None):
    if condition is None:
        return False
    try:
        mongo.db.user.update(condition, {"$set":{"using":False}})
    except:
        return False
    return True


def request_to_class(json_request):
    user = User()
    name = json_request.get('name', None)

    information_datas = json_request.get('information', {})
    events_datas = json_request.get('events',[])
    user.name = name
    if information_datas is not None:
        for k, v in information_datas.items():
            if k in user.model['information']:
                user.model['information'][k] = v
    if events_datas is not None:
        for events_data in events_datas:

            event = Event()
            for k, v in events_data.items():
                if k in event.model:
                    event.model[k] = v
            user.events.append(event)
    return user

def update_user(mongo, condition=None, change_items = None):
    if condition is None:
        return False
    try:
        mongo.db.user.update(condition, {"$set":change_items})
    except:
        return False
    return True

def to_json_list(user):
    _id = user.get('_id', None)
    name = user.get('name', None)
    information = user.get('information', {})
    events=user.get('events',[])
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

def insert_event(json_request,mongo,_id):
    try:
        condition={'using':True,'_id':ObjectId(_id)}
    except:
        return None
    event = request_to_class_event(json_request)
    try:
        user_datas = mongo.db.user.find_one(condition)
    except:
        return None
    user_datas["events"].append(event.model)
    number_event(user_datas["events"])
    try:
        mongo.db.user.update(condition, {"$set": {"events": user_datas["events"]}})
        return True
    except:
        return False

def find_event(mongo,_id,event_id):
    try:
        condition_user={'using':True,'_id':ObjectId(_id)}
    except:
        return None
    user_datas = mongo.db.user.find_one(condition_user)
    if user_datas is None:
        return None
    for event_data in user_datas["events"]:
        if event_data["event_id"]==event_id:
            return event_data
    return None

def delete_event(mongo,_id,event_id):
    try:
        condition_user={'using':True,'_id':ObjectId(_id)}
    except:
        return False
        user_datas = mongo.db.user.find_one(condition_user)
    if user_datas is None:
        return None
    for event_data in user_datas["events"]:
        if event_data["event_id"]==event_id:
            event_data["event_using"]=False
            break
    try:
        mongo.db.user.update(condition_user, {"$set":{"events":user_datas["events"]}})
    except:
        return False

def update_event(mongo,_id,event_id,json_request):
    event = request_to_class_event(json_request)
    try:
        condition_user={'using':True,'_id':ObjectId(_id)}
    except:
        return False
    user_datas = mongo.db.user.find_one(condition_user)
    if user_datas is None:
        return None
    for event_data in user_datas["events"]:
        if event_data["event_id"]==event_id:
            user_datas["events"].remove(event_data)
            break
    user_datas["events"].append(event.model)
    number_event(user_datas["events"])
    try:
        mongo.db.user.update(condition_user, {"$set": {"events": user_datas["events"]}})
        return True
    except:
        return False