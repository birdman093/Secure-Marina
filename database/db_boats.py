from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename
from routes.helper.pagination import *

client = datastore.Client()

def AddBoatToDb(boatData: dict, owner: str) -> Tuple[int, str]:
    '''
    201 Created
    '''
    newboat = datastore.entity.Entity(key=client.key(boatstablename))
    newboat.update({
        "name": boatData["name"],
        "type": boatData["type"],
        "length": boatData["length"],
        "public": boatData["public"],
        "owner": owner
    })
    client.put(newboat)
    newboat["id"] = newboat.key.id
    return 201, json.dumps(newboat)
    
def GetAllFromDbByOwnerSub(ownerSub: str) -> list:
    '''
    if ownerSub == "" -> return all public boats
    else returns all boats belonged to by owner
    '''
    if ownerSub == "":
        query = client.query(kind=boatstablename)
        query.add_filter('public', '=', True)
    else:
        query = client.query(kind=boatstablename)
        query.add_filter('owner', '=', ownerSub)
    res = list(query.fetch())
    for item in res:
        item["id"] = item.key.id
    return res

def GetOwnerBoatsandPublicFromDb(ownerid: str) -> Tuple[int, str]:
    '''
    200 OK
    '''
    query = client.query(kind=boatstablename)
    query.add_filter('owner', '=', ownerid)
    query.add_filter('public', '=', True)
    res = list(query.fetch())
    for item in res:
        item["id"] = item.key.id
    return res
             
def DeleteFromDb(id: str, ownersub:str) -> Tuple[int]:
    '''
    204 Created
    403 Forbidden (boat does not belong to owner)
    404 Not Found
    '''
    key = client.key(boatstablename, int(id))
    entity = client.get(key=key)
    if entity and entity['owner'] != ownersub:
        return 403
    elif entity:
        client.delete(key)
        return 204
    else:
        return 404