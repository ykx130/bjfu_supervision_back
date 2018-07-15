from flask import jsonify, request
from app.http.handler.form_meta import form_meta_blueprint
from run import mongo
from flask_pymongo import ObjectId


@form_meta_blueprint.route('/form_metas', methods=['POST'])
def new_form_meta():
    print('1111')

@form_meta_blueprint.route('/form_metas')
def form_metas():
    return jsonify({'test':'1111'})





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