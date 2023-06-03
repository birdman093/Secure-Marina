from flask import request, jsonify, Blueprint
import json

from database.db_loads import *
from database.db import *
from credentials.names import *
from routes.helper.validation import *
from routes.helper.jwt_verify import verify_jwt
from routes.helper.error_msg import geterrormsg

bp = Blueprint('loads', __name__, url_prefix='/loads')

@bp.route('/', methods=['POST'])
def post_load():
    '''
    Create Load; JWT not required

    Successful: 201
    Unsuccessful: 400, 401 (JWT), 406
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    loaddata = request.get_json()

    statuscode,load = AddLoadToDb(loaddata)
    if statuscode == 201:
        res = make_response(load)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(load))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

@bp.route('/<loadId>', methods=['GET'])
def get_load(loadId):
    '''
    Get Load by ID

    Successful: 200
    Unsuccessful: 404
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    statuscode, load = GetLoadFromDb(loadId, loadtablename)
    if statuscode == 200:
        res = make_response(load)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(load))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res


@bp.route('/', methods=['GET'])
def get_loads():
    '''
    Get All Loads (Supports Pagination);

    Successful: 200
    Unsuccessful:
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    loads = GetAllFromDb_Pagination(loadtablename, "")
    return json.loads(loads), 200

@bp.route('/<loadId>', methods=['DELETE'])
def delete_load(loadId):
    '''
    Delete Load; Requires JWT if load on boat

    Successful: 204
    Unsuccessful: 400, 403, 404
    '''

    payload = verify_jwt(request, True) # 401 on error
    if not payload:
        sub = ""
    else:
        sub = payload['sub']

    statuscode, msg = DeleteLoadFromDb(loadId, loadtablename)
    if statuscode == 204:
        res = make_response()
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(msg))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    
@bp.route('/<loadId>', methods=['PATCH'])
def patch_load(loadId):
    '''
    Patch Load; Requires JWT if load on boat

    Successful: 201
    Unsuccessful: 400, 403, 404, 406
    '''

    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    loaddata = request.get_json()
    payload = verify_jwt(request, True)
    if not payload:
        sub = ""
    else:
        sub = payload['sub']

    statuscode,load = EditLoadFromDb(loadId, loaddata, sub, False)
    if statuscode == 201:
        res = make_response(load)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(load))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

@bp.route('/<loadId>', methods=['PUT'])
def put_load(loadId):
    '''
    Put Load; Requires JWT if load on boat

    Successful: 201
    Unsuccessful: 400, 403, 404, 406
    '''

    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    loaddata = request.get_json()
    payload = verify_jwt(request, True) # 401 on error
    sub = payload['sub']

    statuscode,load = EditLoadFromDb(loadId, loaddata, sub, True)
    if statuscode == 201:
        res = make_response(load)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(load))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

@bp.errorhandler(405)
def method_not_allowed(e):
    return 'Method not allowed', 405