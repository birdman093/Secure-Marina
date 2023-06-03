from flask import Flask
import routes.boats as boats, routes.loads as loads, routes.oauth as login
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
