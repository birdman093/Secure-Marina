from flask import request, jsonify, Blueprint, make_response
import json

from database.db_boats import *
from database.db import *
from credentials.names import *
from routes.helper.validation import *
from routes.helper.jwt_verify import verify_jwt, AuthError
from routes.helper.error_msg import geterrormsg

bp = Blueprint('boats', __name__, url_prefix='/boats')
 
@bp.route('/', methods=['POST'])
def post_boat():
    '''
    Creates Boat, Requires JWT
    Sends Boat back in Response

    Successful Codes: 201
    Unsuccessuful Codes: 400, 401 (JWT), 406
    '''

    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    payload = verify_jwt(request) # 401 on error
    sub = payload['sub']
    boat = request.get_json()

    statuscode, boat = AddBoatToDb(boat,sub)
    if statuscode == 201:
        res = make_response(boat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(boat))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

@bp.route('/<boatId>', methods=['GET'])
def get_boat(boatId):
    '''
    Returns Boat Data Given ID; Requires valid JWT to view

    Successful Codes: 200
    Unsuccessful Codes: 401(JWT), 403, 404, 406
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    payload = verify_jwt(request) # returns with 401 error if token not validated
    sub = payload['sub']

    statuscode, boat = GetBoatByOwnerandID(sub, boatId)
    if statuscode == 200:
        res = make_response(boat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(geterrormsg(boatstablename, statuscode))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    

@bp.route('/', methods=['GET'])
def get_boats():
    '''
    Get Boats w/ Pagination; Requires valid JWT to view

    Successful Codes: 200
    Unsuccessful Codes: 401(JWT)
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    payload = verify_jwt(request) # returns with 401 error if token not validated
    sub = payload['sub']

    boats : str = GetAllFromDb_Pagination(boatstablename, sub)
    return json.loads(boats), 200

@bp.route('/<boatId>', methods=['DELETE'])
def delete_boat(boatId):
    '''
    Delete Boat; Requires valid JWT

    Successful Codes: 204
    Unsuccessuful Codes: 401 (JWT), 403, 404
    '''

    payload = verify_jwt(request) # returns with 401 error if token not validated
    sub = payload['sub']

    statuscode = DeleteFromDb(boatId, sub)
    if statuscode == 204:
        res = make_response()
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(geterrormsg(boatstablename, statuscode))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res 
    
@bp.route('/<boatId>', methods=['PATCH'])
def patch_boat(boatId):
    '''
    Patch Boat; Requires valid JWT

    Successful Codes: 201
    Unsuccessuful Codes: 400, 401 (JWT), 403, 404
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    payload = verify_jwt(request) # returns with 401 error if token not validated
    sub = payload['sub']
    boat = request.get_json()

    statuscode, editboat = EditBoatFromDb(boatId, boat, sub, False)
    if statuscode == 201:
        res = make_response(editboat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(editboat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res 


@bp.route('/<boatId>', methods=['PUT'])
def put_boat(boatId):
    '''
    Put Boat; Requires valid JWT

    Successful Codes: 201
    Unsuccessuful Codes: 400, 401 (JWT), 403, 404
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    payload = verify_jwt(request) # returns with 401 error if token not validated
    sub = payload['sub']
    boat = request.get_json()

    statuscode, editboat = EditBoatFromDb(boatId, boat, sub, True)
    if statuscode == 201:
        res = make_response(editboat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(editboat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res 

@bp.route('/<boatId>/loads/<loadId>', methods=['PUT'])
def add_load_on_boat(boatId, loadId):
    '''
    Add a load to a boat;
    Requires valid JWT

    Successful: 204
    Unsuccessful: 400, 401 (JWT), 403, 404
    '''

    payload = verify_jwt(request) # returns with 401 error if token not validated
    owner = payload['sub']

    statuscode, msg = AddLoadToBoatDb(boatId, loadId, owner)
    if statuscode == 204:
        res = make_response()
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(msg)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    
@bp.route('/<boatId>/loads/<loadId>', methods=['DELETE'])
def del_load_on_boat(boatId, loadId):
    '''
    Delete a load from boat;
    Requires valid JWT

    Successful: 204
    Unsuccessful: 400, 401 (JWT), 403, 404
    '''

    payload = verify_jwt(request) # returns with 401 error if token not validated
    owner = payload['sub']

    statuscode, msg = DeleteLoadFromBoatDb(boatId, loadId, owner)
    if statuscode == 204:
        res = make_response()
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(msg)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

