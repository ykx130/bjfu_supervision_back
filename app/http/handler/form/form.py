from app.http.handler.form import form_blueprint
from flask import jsonify, request, url_for
from app.core.controllers.form_controller import to_json_list, find_form, delete_form, insert_form,update_form, request_to_class, find_forms
from flask_pymongo import ObjectId
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit, object_to_str
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError


@form_blueprint.route('/forms', methods=['POST'])
def new_form():
    from run import mongo
    form = request_to_class(request.json)
    try:
        insert_form(mongo, form)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'form':None
        }),500
    return jsonify({
        'code':200,
        'message':'',
        'form':None
    }),200


@form_blueprint.route('/forms')
def get_forms():
    url_condition = UrlCondition(request.args)
    from run import mongo
    try:
        forms = find_forms(mongo, url_condition.filter_dict)
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'forms':None
        }),500
    forms = sort_limit(forms, url_condition.sort_limit_dict)
    paginate = Paginate(forms, url_condition.page_dict)
    forms_list = [to_json_list(form) for form in paginate.data_page]
    prev = None
    if paginate.has_prev:
        prev = url_for('form_blueprint.get_forms', _page=paginate.page - 1)
    next = None
    if paginate.has_next:
        next = url_for('form_blueprint.get_forms', _page=paginate.page + 1)
    return jsonify({
        'code': 200,
        'message': '',
        'forms': [object_to_str(forms_list_node) for forms_list_node in forms_list],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
    }),200


@form_blueprint.route('/forms/<string:_id>')
def get_form(_id):
    from run import mongo
    try:
        form = find_form(mongo, _id)
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'form':None
        }),500
    if form is None:
        return jsonify({
            'code':404,
            "message":'Not found',
            'form':None
        }),404
    return jsonify({
        'code':200,
        'message':'',
        'form':object_to_str(form) if form is not None else None
    }),200


@form_blueprint.route('/forms/<string:_id>', methods=['DELETE'])
def delete_from(_id):
    from run import mongo
    form = find_form(mongo, _id)
    if form is None:
        return jsonify({
            'code':404,
            'message':"not found",
            'form':None
        }),404
    try:
        delete_form(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':'',
            'form':None
        })
    return jsonify({
        'code':200,
        'message':'',
        'form':None
    })


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
def change_form(_id):
    from run import mongo
    form = find_form(mongo, _id)
    if form is None:
        return jsonify({
            'code':404,
            'message':'no this form',
            'form':None
        }),404
    try:
        update_form(mongo, {'_id':ObjectId(_id)}, request.json)
    except:
        return jsonify({
            'code':500,
            'message':'',
            'form':None
        }),500
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }),200
