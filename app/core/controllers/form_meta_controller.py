from app.core.models import FormMeta, Item

def find_form_meta(mongo, condition= None):
    if condition is None:
        return mongo.db.form_meta.find()
    datas = mongo.db.form_meta.find(condition)
    return datas
#传入字典型返回筛选过的数据的cursor, 遍历cursor得到的是字典

def insert_form_meta(mongo, form_meta):
    form_meta.items_to_dict()
    mongo.db.form_meta.insert(form_meta.model)

def delete_form_meta(mongo, condition= None):
    if condition is None:
        return False
    mongo.db.form_meta.update(condition, {"$set":{"using":False}})

def request_to_class(json_request):
    form_meta = FormMeta()

    meta = json_request.get('meta', None)
    item_datas = json_request.get('items', None)
    if meta is not None:
        form_meta.meta = meta
    if item_datas is not None:
        for item_data in item_datas:
            pass




# {
#   "meta": {
#     "version": ""
#   },
#   "items":[
#     {
#       "item_name":"",
#       "item_type":"",
#       "extra":"",
#       "type":"",
#       "payload":{
#         "options":[]
#       }
#     }
#   ]
# }