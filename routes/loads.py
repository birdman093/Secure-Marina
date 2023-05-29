from flask import request, jsonify, Blueprint
import json

from database.db_loads import *
from database.db import *
from credentials.names import *
from routes.helper.error_msg import errorMissingLoad

bp = Blueprint('loads', __name__, url_prefix='/loads')

# 5.) Create a load
@bp.route('/', methods=['POST'])
def post_load():
    loaddata = request.get_json();
    res,load = AddLoadToDb(loaddata)
    if res:
        return json.loads(load), 201
    else:
        return jsonify({"Error": "The request object is missing at least one of the required attributes"}), 400

# 6.) Get a load with ID
@bp.route('/<loadId>', methods=['GET'])
def get_load(loadId):
    res, load = GetFromDb(loadId, loadtablename)
    if res:
        return json.loads(load), 200
    else:
        return jsonify(errorMissingLoad), 404

# 7.) Get all loads. supports pagination
@bp.route('/', methods=['GET'])
def get_loads():
    #todo: thing
    loads = GetAllFromDb_Pagination(loadtablename, "")
    return json.loads(loads), 200

# 8.) delete a load
@bp.route('/<loadId>', methods=['DELETE'])
def delete_load(loadId):
    resbool = DeleteFromDb(loadId, loadtablename)
    if resbool:
        return jsonify({}), 204
    else:
        return jsonify(errorMissingLoad), 404