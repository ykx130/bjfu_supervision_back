from flask import jsonify,request,url_for
from app.http.handler.form import form_blueprint
from app.core.controllers.form_controller import find_form,insert_form,request_to_class,to_json_list
from flask_pymongo import ObjectId
from app.core.controllers.common_controller import dict_serializable,UrlCondition,sort_limit,Paginate
from pymongo.errors import ServerSelectionTimeoutError,PyMongoError

@form_blueprint.route('/forms',methods=['POST'])
def new_form():
    from run import mongo
    form=request_to_class(request.json)
    try:
        insert_form(mongo,form)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':'500',
            'message':e,
        })
    dict_json=dict_serializable(form.model)
    return jsonify({
        'code':200,
        'message':'',
        'data':[dict_json]
    })

@form_blueprint.route('/forms/<int:id>',methods=['DELETE'])
def delete_form(_id):
    from run import mongo
    try:
        delete_form(mongo,{'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':'500',
            'message':'',
        })
    return jsonify({
        'code': '200',
        'message': '',
        'data': []
    })

@form_blueprint.route('/forms',methods=['GET'])
def get_forms():
    from run import mongo
    url_condition=UrlCondition(request.args)
    try:
        forms=find_form(mongo,url_condition.filter_dict)
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    forms=sort_limit(forms,url_condition.sort_limit_dict)
    paginate=Paginate(forms,url_condition.page_dict)
    forms_list=[to_json_list(form) for form in paginate.data_page]
    prev=None
    if paginate.has_prev:
        prev=url_for('form_blueprint.get_forms',_page=paginate.page-1)
    next=None
    if paginate.has_next:
        next=url_for('form_blueprint.get_forms',_page=paginate.page+1)
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(forms_list_node) for forms_list_node in forms_list],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
    })

@form_blueprint.route('/forms/<int:id>',methods=['GET'])
def get_form(_id):
    from run import mongo
    try:
        forms=find_form(mongo,{'id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': ''
        })
    return jsonify({
        'code': '200',
        'message': '',
        'data': [dict_serializable(form) for form in forms]
    })


@form_blueprint.route('forms/<int:id>',methods=['PUT'])
def modify_form(_id):
    from run import mongo
    try:
        form = find_form(mongo, {'id': ObjectId(_id)})
        delete_form(mongo, {'_id': ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code': '500',
            'message': e
        })
    try:
        insert_form(mongo,form)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code':'500',
            'message':e
        })
    dict_json=dict_serializable(form.model)
    return jsonify({
        'code':200,
        'message':'',
        'data':[dict_json]
    })