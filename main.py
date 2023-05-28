from flask import Flask, request, jsonify, Blueprint
from google.cloud import datastore
from db import *
from responsehelper import *
import boats
import loads

app = Flask(__name__)
app.register_blueprint(boats.bp)
app.register_blueprint(loads.bp)

@app.route('/', methods=['GET'])
def greeting():
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
