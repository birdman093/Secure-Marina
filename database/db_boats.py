from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename
from routes.helper.pagination import *

client = datastore.Client()

def AddBoatToDb(boatData: dict, owner: str) -> Tuple[int, str]:
    '''
    201 Created
    400 Missing Attribute
    '''
    # TODO: validate inputs here
    if "name" in boatData and "type" in boatData and "length" in boatData:
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
        return 400, ""
    
def GetBoatById(ownerSub: str) -> list:
    '''
    Returns all boats belonged to by owner
    '''

    #todo: Get boat by ID if owner valid
    query = client.query(kind=boatstablename)
    query.add_filter('owner', '=', ownerSub)
    res = list(query.fetch())
    for item in res:
        item["id"] = item.key.id
        item["self"] = geturl(item.key.id, boatstablename)
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

def EditBoatFromDb(boatId,boatData) -> Tuple[bool, bool, str]:

    #todo: Update to use owner, etc.
    key = client.key(boatstablename, int(boatId))
    boat = client.get(key=key)
    if boat:
        if "name" not in boatData or "type" not in boatData or \
        "length" not in boatData:
            return True, False, ""
        else:
            boat.update({
            "name": boatData["name"],
            "type": boatData["type"],
            "length": boatData["length"]
            })
            client.put(boat)
            return True, True, json.dumps(boat)
    else:
        return False, False, ""
    
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