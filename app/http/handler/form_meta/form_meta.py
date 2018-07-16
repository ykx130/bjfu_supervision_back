from flask import jsonify, request
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers.form_meta_controller import find_form_meta, delete_form_meta, insert_form_meta, request_to_class,\
    dict_serializable, to_json_list
from flask_pymongo import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

@form_meta_blueprint.route('/form_metas', methods=['POST'])
def new_form_meta():
    from run import mongo
    form_meta = request_to_class(request.json)
    try:
        insert_form_meta(mongo, form_meta)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    dict_json = dict_serializable(form_meta.model)
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_json]
    })

@form_meta_blueprint.route('/form_metas')
def get_form_metas():
    from run import mongo
    try:
        form_metas = find_form_meta(mongo)
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message': e
        })
    form_metas_list = [to_json_list(form_meta) for form_meta in form_metas]
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(form_metas_list_node) for form_metas_list_node in form_metas_list]
    })

@form_meta_blueprint.route('/form_metas/<string:_id>')
def get_form_meta(_id):
    from run import mongo
    try:
        form_metas = find_form_meta(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':''
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[dict_serializable(form_meta) for form_meta in form_metas]
    })


@form_meta_blueprint.route('/form_metas/<string:_id>', methods=['DELETE'])
def delete_from_meta(_id):
    from run import mongo
    try:
        delete_form_meta(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':'',
        })
    return jsonify({
        'code':'200',
        'message':'',
        'data':[]
    })
