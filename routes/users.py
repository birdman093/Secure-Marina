from flask import Blueprint
from database.db_users import *
from credentials.names import *
from routes.helper.jwt_verify import verify_jwt
import json

bp = Blueprint('users', __name__, url_prefix='/users')

# Get All Users 
@bp.route('/', methods=['GET'])
def get_users():
    '''
    Get Users

    Successful Codes: 200
    '''
    if not validateMime(request.accept_mimetypes,[jsonmime]): 
        res = make_response(jsonify(geterrormsg(boatstablename, 406)))
        res.mimetype = 'application/json'
        res.status_code = 406
        return res

    users : list[dict] = GetUsersFromDb()
    res = make_response(jsonify(users))
    res.status_code = 200
    return res
