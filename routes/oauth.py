from flask import Flask, request, jsonify, Blueprint, render_template, session, url_for, redirect
from database.db_loads import *
from credentials.names import *
from google.cloud import datastore
from routes.helper.jwt_verify import AuthError, verify_jwt
from flask_cors import cross_origin
from functools import wraps
from six import *
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from database.db_users import *

from credentials.credentials import CLIENT_ID, CLIENT_SECRET, DOMAIN

bp = Blueprint('login', __name__, url_prefix='')
oauth = None
auth0 = None

def setup_oauth(app):
    global oauth
    global auth0

    oauth = OAuth(app)
    auth0 = oauth.register(
        "auth0",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        api_base_url="https://" + DOMAIN,
        access_token_url="https://" + DOMAIN + "/oauth/token",
        authorize_url="https://" + DOMAIN + "/authorize",
        client_kwargs={
            'scope': 'openid profile email',
        },
        server_metadata_url=f'https://{DOMAIN}/.well-known/openid-configuration'
    )

@bp.route('/')
def home():
    token = request.args.get('token')
    return render_template('index.html')        

@bp.route("/login")
def login():
    print(f'**** login {url_for("login.callback", _external=True)} ****')
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("login.callback", _external=True)
    )

@bp.route("/callback", methods=["GET", "POST"])
def callback():
    print("**** callback ****")
    token = oauth.auth0.authorize_access_token() # issue here
    session["user"] = token
    print("**** we got token ****")
    AddUserToDb(token)
    return redirect("/?token="+token['id_token'])

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login.home", _external=True),
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response