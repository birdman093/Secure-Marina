from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename
from routes.helper.pagination import *
from routes.helper.validation import *
from routes.helper.error_msg import *

client = datastore.Client()

def AddBoatToDb(boatData: dict, owner: str) -> Tuple[int, str]:
    '''
    201 Created
    400 Missing/ Invalid Attribute

    Status Code, New Boat/ Error Msg
    '''
    valid, error = validateboatinputs(boatData)
    if valid:
        newboat = datastore.entity.Entity(key=client.key(boatstablename))
        newboat.update({
            "name": boatData["name"],
            "type": boatData["type"],
            "length": boatData["length"],
            "owner": owner,
            "loads": []
        })
        client.put(newboat)
        newboat["id"] = newboat.key.id
        newboat["self"] = geturl(newboat.key.id, boatstablename)
        return 201, json.dumps(newboat)
    else:
        return 400, error

def GetBoatByOwnerandID(ownerSub: str, boatId: int) -> Tuple[int, str]:
    '''
    Returns all boats belonged to by owner.

    Successful: 200
    Unsuccessful: 403, 404
    '''

    key = client.key(boatstablename, int(boatId))
    entity = client.get(key=key)
    if entity and entity['owner'] == ownerSub:
        entity["id"] = entity.key.id
        entity["self"] = geturl(entity.key.id, boatstablename)
        return 200, json.dumps(entity)
    elif entity:
        return 403, ""
    else:
        return 404, ""
             
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

def EditBoatFromDb(boatId, boatData, owner, allinputsreqd) -> Tuple[int, str]:
    '''
    Successful: 201
    Unsuccessful: 400, 403, 404
    '''

    inputsprovided, msg = validateboatinputs(boatData, allinputsreqd)
    if not inputsprovided: return 400, msg

    key = client.key(boatstablename, int(boatId))
    boat = client.get(key=key)
    if boat and boat["owner"] == owner:
        boat.update({
        "name": boatData["name"],
        "type": boatData["type"],
        "length": boatData["length"]
        })
        client.put(boat)
        return 201, json.dumps(boat)
    elif boat and boat["owner"] != owner:
        return 403, geterrormsg(403, boatstablename)
    else:
        return 404, geterrormsg(404, boatstablename)
    
# Add Load to Boat 
def AddLoadToBoatDb(boatId, loadId) -> Tuple[bool, bool]:
    keyboat = client.key(boatstablename, int(boatId))
    boat = client.get(key=keyboat)
    keyload = client.key(loadtablename, int(loadId))
    load = client.get(key=keyload)

    if not boat or not load:
        return False, False
    elif load["carrier"] == None and not any(int(loadId) == int(loadRef["id"]) for loadRef in boat["loads"]):
        
        with client.transaction():
            # add load to boat
            boat["loads"].append({  "id": load.key.id,
                                    "self": geturl(load.key.id, loadtablename)})
            boat.update({ "loads": boat["loads"]})
            client.put(boat)

            # add boat to load
            load.update({
                "carrier": {"id": boat.key.id,
                            "name": boat["name"],
                            "self": geturl(boat.key.id, boatstablename)}
            })
            client.put(load)

        return True, True
    else:
        return True, False
 
def DeleteLoadFromBoatDb(boatId, loadId) -> Tuple[bool, bool]:
    keyboat = client.key(boatstablename, int(boatId))
    boat = client.get(key=keyboat)
    keyload = client.key(loadtablename, int(loadId))
    load = client.get(key=keyload)

    if not boat or not load:
        return False, False
    elif load["carrier"] != None and any(int(loadId) == int(loadRef["id"]) for loadRef in boat["loads"]):
        with client.transaction():
            # remove load from boat
            index = next((i for i, loadRef in enumerate(boat["loads"]) if int(loadId) == int(loadRef["id"])), None)
            boat["loads"].pop(index)
            boat.update({ "loads": boat["loads"]})
            client.put(boat)

            #remove boat from load
            load.update({
                "carrier": None
            })
            client.put(load)

        return True, True
    else:
        return True, False