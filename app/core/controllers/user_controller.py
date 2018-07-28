from app.core.models import User,Event
from flask_pymongo import ObjectId
import json


def find_user(mongo, condition=None):
    if condition is None:
        return mongo.db.user.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.user.find(condition)
    return datas


def insert_user(mongo, user):
    user.events_to_dict()
    #??????????????????????????????????????????????????????
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
    id = json_request.get('id', None)
    name = json_request.get('name', {})
    information_datas = json_request.get('information', {})
    events_datas=json_request.get('events',[])
    user.id = id
    user.name=name
    if information_datas is not None:
        user.information = information_datas
    if events_datas is not None:
        for events_data in events_datas:
            event=Event()
            for k,v in events_data.events():
                #?????????????????????????????????????????????????????
                if k in event.model:
                    event.model[k]=v
            user.events.append(event)
    return user


def to_json_list(user):
    _id = user.get('_id', None)
    name = user.get('name', None)
    information = user.get('information', {})
    events=user.get('events',[])
    using = user.get('using', None)
    json_list = {
        '_id': _id,
        'name ': name ,
        'information': information,
        'events':events,
        'using': using
    }
    return json_list

def request_to_class_event(json_request):
    events = []
    event=Event()
    event_id = json_request.get('event_id', None)
    time = json_request.get('time', None)
    value = json_request.get('value', None)
    descripe = json_request.get('descripe', None)
    event.event_id = event_id
    event.time=time
    event.value=value
    event.descripe=descripe
    events.append(event)
    return events

def update_event(mongo,events,condition=None):
    event_datas=mongo.db.user.find(condition,{events:1})
    events.append(event_datas)
    mongo.db.user.update(condition,{"$set":{"events":events}})
    datas = mongo.db.user.find(condition)
    return datas

def find_event(mongo,condition):
    event = mongo.db.user.find(condition,{"events":1})
    return event

def delete_event(mongo,condition):
    try:
        mongo.db.user.update(condition, {"$set":{"event_using":False}})
    except:
        return False
    return True