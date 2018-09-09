from app.http.handler.form import form_blueprint
from flask import jsonify, request
from app.core.controllers.form_controller import to_json_list, find_form, delete_form, insert_form, update_form, \
    request_to_class, find_forms
from flask_pymongo import ObjectId
from app.utils.url_condition.url_condition_mongodb import UrlCondition, Paginate, sort_limit, object_to_str


@form_blueprint.route('/forms', methods=['POST'])
def new_form():
    from run import mongo
    form = request_to_class(request.json)
    (_, err) = insert_form(mongo, form)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        })
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200


@form_blueprint.route('/forms')
def get_forms():
    url_condition = UrlCondition(request.args)
    from run import mongo
    (forms, err) = find_forms(mongo, url_condition.filter_dict)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'forms': []
        }), 500
    forms = sort_limit(forms, url_condition.sort_limit_dict)
    paginate = Paginate(forms, url_condition.page_dict)
    forms_list = [to_json_list(form) for form in paginate.data_page]
    return jsonify({
        'code': 200,
        'message': '',
        'forms': [object_to_str(forms_list_node) for forms_list_node in forms_list],
        'total': paginate.total,
    }), 200


@form_blueprint.route('/forms/<string:_id>')
def get_form(_id):
    from run import mongo
    (form, err) = find_form(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            "message": 'Not found',
            'form': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'form': object_to_str(form) if form is not None else None
    }), 200


@form_blueprint.route('/forms/<string:_id>', methods=['DELETE'])
def delete_from(_id):
    from run import mongo
    (form, err) = find_form(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form': None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            'message': "not found",
            'form': None
        }), 404
    (_, err) = delete_form(mongo, {'_id': ObjectId(_id)})
    if err is not None:
        return jsonify({
            'code':500,
            'message':str(err),
            'form':None
        }),500
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    })


@form_blueprint.route('/forms/<string:_id>', methods=['PUT'])
def change_form(_id):
    from run import mongo
    (form, err) = find_form(mongo, _id)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form':None
        }), 500
    if form is None:
        return jsonify({
            'code': 404,
            'message': 'no this form',
            'form': None
        }), 404
    (_, err) = update_form(mongo, {'_id': ObjectId(_id)}, request.json)
    if err is not None:
        return jsonify({
            'code':500,
            'message':str(err),
            'form':None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form': None
    }), 200
