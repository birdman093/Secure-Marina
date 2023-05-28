from flask import Flask, request, jsonify, Blueprint
from google.cloud import datastore
from db import *
from responsehelper import *
import json

bp = Blueprint('boats', __name__, url_prefix='/boats')

# 1.) Create a boat 
@bp.route('/', methods=['POST'])
def post_boat():
    boat = request.get_json();
    res,boat = AddBoatToDb(boat)
    if res:
        return json.loads(boat), 201
    else:
        return jsonify(errorMissingAttribute), 400

# 2.) View a boat with id
@bp.route('/<boatId>', methods=['GET'])
def get_boat(boatId):
    res, boat = GetFromDb(boatId, boatstablename)
    if res:
        return json.loads(boat), 200
    else:
        return jsonify(errorMissingBoat), 404

# 3.) View all boats (supports pagination)
@bp.route('/', methods=['GET'])
def get_boats():
    boats : str = GetAllFromDb(boatstablename)
    return json.loads(boats), 200

# 4.) Delete a boat
@bp.route('/<boatId>', methods=['DELETE'])
def delete_boat(boatId):
    resbool = DeleteFromDb(boatId, boatstablename)
    if resbool:
        return jsonify({}), 204
    else:
        return jsonify(errorMissingBoat), 404

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



