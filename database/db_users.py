from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename, baseurl
from routes.helper.pagination import *
from routes.helper.validation import *
from routes.helper.error_msg import *

client = datastore.Client()

def AddUserToDb(user_data) -> None:
    '''
    Add User

    BackEnd Only DB Add
    '''
    # check if sub is in datastore
    sub = user_data["userinfo"]["sub"]
    query = client.query(kind=usertablename)
    query.key_filter(client.key(usertablename, sub), '=')
    results = list(query.fetch())
    if len(results) > 0:
        print("not added")
        return

    user = datastore.entity.Entity(key=client.key(usertablename, sub))
    user.update({
        "nickname": user_data["userinfo"]["nickname"],
        "email": user_data["userinfo"]["email"],
        "sub": user_data["userinfo"]["sub"]
    })
    client.put(user)
    print("added")
    print("user")
    

def GetUsersFromDb() -> Tuple[int, str]:
    '''
    Add User

    Successful: 200
    Unsuccessful: 400
    '''
    # Create a query on the kind
    query = client.query(kind=usertablename)
    results = list(query.fetch())
    users = [{k: v for k, v in dict(entity).items() if k != '__key__'} for entity in results]
    print(users)
    return 200, json.dumps(users)
