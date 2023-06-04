from flask import Flask, jsonify
import routes.boats as boats, routes.loads as loads, routes.oauth as login
from routes.helper.jwt_verify import AuthError
import routes.users as users
from credentials.credentials import FLASK_SECRET_KEY

# set up flask server with oauth
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.register_blueprint(boats.bp)
app.register_blueprint(loads.bp)
app.register_blueprint(login.bp)
app.register_blueprint(users.bp)
login.setup_oauth(app)

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    return 'Method not allowed', 405

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
