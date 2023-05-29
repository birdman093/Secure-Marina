from flask import Flask, request, jsonify, Blueprint, make_response
from database.db_loads import *
from database.db_boats import *
from credentials.names import *
from routes.helper.jwt_verify import verify_jwt
import json
from routes.helper.error_msg import errorMessage, errorLoadOnBoat, errorMissingOne, errorMissingAttribute, errorMissingBoat, errorBoatLoad

bp = Blueprint('boats', __name__, url_prefix='/boats')

# Create Boat 
@bp.route('/', methods=['POST'])
def post_boat():
    '''
    Successful Codes: 201
    Unsuccessuful Codes; 401 (JWT)

    Validates JWT to create a Boat
    '''
    payload = verify_jwt(request) # returns with 401 error if token not validated
    boat = request.get_json()
    sub = payload['sub']

    statuscode, boat = AddBoatToDb(boat,sub)
    if statuscode == 201:
        res = make_response(boat)
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res
    else:
        res = make_response(jsonify(errorMessage[statuscode]))
        res.mimetype = 'application/json'
        res.status_code = statuscode
        return res

# Get Boats by ID
@bp.route('/<boatId>', methods=['GET'])
def get_boat(boatId):
    '''
    Successful Codes: 200
    '''
    
    # TODO: JWT
    ''' JWT
    publicflag = True
    payload = verify_jwt(request, True) # returns with 401 error if token not validated
    if payload != None:
        sub = payload['sub']
    else:
        sub = ""
    '''

    # validate inputs
    sub = ""
    boats = GetAllFromDbByOwnerSub(sub) # sub = "" if public
    res = make_response(boats)
    res.status_code = 200
    return res
    

# Get All boats (supports pagination)
@bp.route('/', methods=['GET'])
def get_boats():
    #TODO: JWT
    boats : str = GetAllFromDb(boatstablename)
    return json.loads(boats), 200

# 4.) Delete a boat
@bp.route('/<boatId>', methods=['DELETE'])
def delete_boat(boatId):
    '''
    Successful Codes: 204
    Unsuccessuful Codes; 400, 403

    Validates JWT to Delete Boat
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
        res = make_response(errorMessage[statuscode])
        res.mimetype = 'application/json'
        res.status_code = 403
        return res 

# 9.) Add a load to a boat 
@bp.route('/<boatId>/loads/<loadId>', methods=['PUT'])
def add_load_on_boat(boatId, loadId):
    resFound, resEdit = AddLoadToBoatDb(boatId, loadId)
    if resFound and resEdit: # success
        return jsonify({}), 204
    elif resFound: # cannot perform action
        return jsonify(errorLoadOnBoat), 403
    else: # missing boat or load
        return jsonify(errorMissingOne), 404
    
# 9.) Delete a load to a boat 
@bp.route('/<boatId>/loads/<loadId>', methods=['DELETE'])
def del_load_on_boat(boatId, loadId):
    resFound, resEdit = DeleteLoadFromBoatDb(boatId, loadId)
    if resFound and resEdit: # success
        return jsonify({}), 204
    else: # missing boat or load
        return jsonify(errorBoatLoad), 404
    
# 10.) View all loads on a boat
@bp.route('/<boatId>/loads', methods=['GET'])
def get_loads_on_boat(boatId):
    resFound, loads = GetSpecificFromDb(boatId, boatstablename, "loads")
    if resFound:
        return json.loads(loads), 200
    else: # missing boat
        return jsonify(errorMissingBoat), 404


@bp.errorhandler(405)
def method_not_allowed(e):
    return 'Method not allowed', 405
