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
        return 406, geterrormsg(boatstablename, 406)

    users : list[dict] = GetUsersFromDb()
    print(users)
    return jsonify(users), 200