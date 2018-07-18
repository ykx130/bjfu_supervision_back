from flask_pymongo import ObjectId


def find_form(mongo, condition=None):
    if condition is None:
        return mongo.db.form.find()
    if '_id' in condition:
        condition['_id']['$in'] = [ObjectId(item) for item in condition['_id']['$in']]
    datas = mongo.db.form_meta.find(condition)
    return datas


def insert_form(mongo, form):
    mongo.db.form_meta.insert(form.model)