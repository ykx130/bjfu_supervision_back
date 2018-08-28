from flask import jsonify, request, url_for
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers.form_meta_controller import find_form_meta, delete_form_meta, insert_form_meta, \
    request_to_class, \
    to_json_list, find_form_metas
from flask_pymongo import ObjectId
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit, object_to_str
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError, OperationFailure


@form_meta_blueprint.route('/form_metas', methods=['POST'])
def new_form_meta():
    from run import mongo
    print(request.json)
    if 'name' and 'version' not in request.json:
        return jsonify({
            'code': 500,
            'message': 'name or version can not be null',
            'form_meta': None
        }), 200
    (old_form_meta, err) = find_form_meta(mongo, request.json['name'])
    if old_form_meta is not None:
        return jsonify({
            'code': 500,
            'message': 'the name has been used',
            'form_meta': None
        }), 200
    form_meta = request_to_class(request.json)
    (ifSuccess, err) = insert_form_meta(mongo, form_meta)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200


@form_meta_blueprint.route('/form_metas')
def get_form_metas():
    url_condition = UrlCondition(request.args)
    from run import mongo
    (form_metas, err) = find_form_metas(mongo, url_condition.filter_dict)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_metas': []
        }), 500
    form_metas = sort_limit(form_metas, url_condition.sort_limit_dict)
    paginate = Paginate(form_metas, url_condition.page_dict)
    form_metas_list = [to_json_list(form_meta) for form_meta in paginate.data_page]
    return jsonify({
        'code': 200,
        'message': '',
        'form_metas': [object_to_str(form_metas_list_node) for form_metas_list_node in form_metas_list],
        'total': paginate.total,
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>')
def get_form_meta_by_name(name):
    if name is None:
        return jsonify({
            'code': 500,
            'message': 'name can not be null',
            'form_meta': None
        })
    from run import mongo
    (form_meta, err) = find_form_meta(mongo, name)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': object_to_str(form_meta) if form_meta is not None else None
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>/<string:version>')
def get_form_meta(name, version):
    if name is None:
        return jsonify({
            'code': 500,
            'message': 'name can not be null',
            'form_meta': None
        })
    from run import mongo
    (form_meta, err) = find_form_meta(mongo, name, version)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': object_to_str(form_meta) if form_meta is not None else None
    }), 200


@form_meta_blueprint.route('/form_metas/<name>', methods=['DELETE'])
def delete_from_meta(name):
    from run import mongo
    (form_meta, err) = find_form_meta(mongo, name)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    (_, err) = delete_form_meta(mongo, {'name': name})
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200


@form_meta_blueprint.route('/form_metas/<string:name>', methods=['PUT'])
def change_form_meta(name):
    from run import mongo
    (form_meta, err) = find_form_meta(mongo, name)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    if form_meta is None:
        return jsonify({
            'code': 404,
            'message': 'not found',
            'form_meta': None
        }), 404
    (_, err) = delete_form_meta(mongo, {'name': name})
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    form_meta = request_to_class(request.json)
    (_, err) = insert_form_meta(mongo, form_meta)
    if err is not None:
        return jsonify({
            'code': 500,
            'message': str(err),
            'form_meta': None
        }), 500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }), 200
