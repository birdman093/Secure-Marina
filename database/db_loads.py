from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename, baseurl
from routes.helper.pagination import *
from routes.helper.validation import *
from routes.helper.error_msg import *

client = datastore.Client()
    
def AddLoadToDb(load_data) -> Tuple[int, str]:
    '''
    Add Load

    Successful: 201
    Unsuccessful: 400
    '''

    valid_load, msg = validateloadinputs(load_data, True)
    if not valid_load:
        return 400, msg

    newload = datastore.entity.Entity(key=client.key(loadtablename))
    newload.update({
        "item": load_data["item"],
        "volume": load_data["volume"],
        "creation_date": load_data["creation_date"],
        "carrier": None
    })
    client.put(newload)
    newload["id"] = newload.key.id
    newload["self"] = geturl(newload.key.id, loadtablename)
    return 201, json.dumps(newload)

def GetLoadFromDb(id: str) -> Tuple[int, str]:
    '''
    Get Specific load from load DB

    Success: 200
    Unsuccess: 400, 404
    '''

    validId, msg = validateId(id)
    if not validId:
        return 400, msg

    key = client.key(loadtablename, int(id))
    obj = client.get(key=key)
    if obj:
        obj["id"] = obj.key.id
        obj["self"] = geturl(id, loadtablename)
        return 200, json.dumps(obj)
    else:
        return 404, geterrormsg(boatstablename, 404)
             
def DeleteLoadFromDb(id: str, owner:str) -> Tuple[int,str]:
    '''
    Delete from loads DB. Does not delete if user is not owner 
    of the boat load sits on.

    Success: 204
    Unsuccess: 400, 403, 404
    '''
    validId, msg = validateId(id)
    if not validId:
        return 400, msg
    
    key = client.key(loadtablename, int(id))
    entity = client.get(key=key)
    if not OwnerOfBoatHoldingLoad(entity, owner):
        return 403, geterrormsg(loadtablename, 403)

    if entity:
        RemoveLoadFromBoat(entity)
        client.delete(key)
        return 204, ""
    else:
        return 404, geterrormsg(loadtablename, 404)
    
def EditLoadFromDb(loadId, loadData, owner, allinputsreqd) -> Tuple[int, str]:
    '''
    Successful: 201
    Unsuccessful: 400, 403, 404
    '''

    validId, msg = validateId(loadId)
    if not validId:
        return 400, msg

    inputsprovided, msg = validateloadinputs(loadData, allinputsreqd)
    if not inputsprovided: return 400, msg

    key = client.key(loadtablename, int(loadId))
    load = client.get(key=key)
    if not load:
        return 404, geterrormsg(loadtablename, 404)
    
    if not OwnerOfBoatHoldingLoad(load, owner):
        return 403, geterrormsg(loadtablename, 403)
    
    for property in ["volume", "item", "creation_date"]:
        if property in loadData:
            load.update({property: loadData[property]})
    client.put(load)
    return 201, json.dumps(load)

def OwnerOfBoatHoldingLoad(load, owner) -> bool:
    '''
    Returns T/F if load is able to be modified by this owner
    '''
    boatId = load["carrier"]
    if not boatId:
        return True
    
    # get boat
    key = client.key(boatstablename, int(boatId))
    entity = client.get(key=key)
    if entity and entity['owner'] == owner:
        return True
    else:
        return False  


def RemoveLoadFromBoat(load, owner:str) -> None:
    '''
    Removes load from boat
    '''
    if "id" in load["carrier"]:
        boatId = load["carrier"]["id"]
        key = client.key(boatstablename, int(boatId))
        boat = client.get(key=key)
        if boat:
            delIdx = -1
            for idx, loadRef in enumerate(boat["loads"]):
                if int(loadRef["id"]) == int(load.key.id):
                    delIdx = idx
                    break;
            if delIdx != -1:
                boat["loads"].pop(delIdx)
                boat.update({ "loads": boat["loads"]})
                client.put(boat)
