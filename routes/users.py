from flask import Blueprint
from database.db_loads import *
from database.db_boats import *
from credentials.names import *
from routes.helper.jwt_verify import verify_jwt
import json

bp = Blueprint('boats', __name__, url_prefix='/users')

# Get All Users 
@bp.route('/', methods=['GET'])
def get_users():
    pass