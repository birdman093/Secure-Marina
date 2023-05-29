from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename, baseurl
from routes.helper.pagination import *


client = datastore.Client()

def AddBoatToDb(boatData) -> Tuple[bool, str]:
    if "name" in boatData and "type" in boatData and "length" in boatData:
        newboat = datastore.entity.Entity(key=client.key(boatstablename))
        newboat.update({
            "name": boatData["name"],
            "type": boatData["type"],
            "length": boatData["length"],
            "loads": []
        })
        client.put(newboat)
        newboat["id"] = newboat.key.id
        newboat["self"] = geturl(newboat.key.id, boatstablename)
        return True, json.dumps(newboat)
    else:
        return False, ""
    
def AddLoadToDb(loadData) -> Tuple[bool, str]:
    if "item" in loadData and "volume" in loadData and "creation_date" in loadData:
        newload = datastore.entity.Entity(key=client.key(loadtablename))
        newload.update({
            "item": loadData["item"],
            "volume": loadData["volume"],
            "creation_date": loadData["creation_date"],
            "carrier": None
        })
        client.put(newload)
        newload["id"] = newload.key.id
        newload["self"] = geturl(newload.key.id, loadtablename)
        return True, json.dumps(newload)
    else:
        return False, ""

def GetFromDb(id: str, tablename: str) -> Tuple[bool, str]:
    if id == "null":
        return False, None
    key = client.key(tablename, int(id))
    obj = client.get(key=key)
    if obj:
        obj["id"] = obj.key.id
        obj["self"] = geturl(id, tablename)
        return True, json.dumps(obj)
    else:
        return False, None
    
def GetSpecificFromDb(id: str, tablename: str, property:str) -> Tuple[bool, str]:
    if id == "null":
        return False, None
    key = client.key(tablename, int(id))
    obj = client.get(key=key)
    if obj:
        if property == "loads":
            for idx, loadRef in enumerate(obj["loads"]):
                key = client.key(loadtablename, int(loadRef["id"]))
                load = client.get(key=key)
                obj["loads"][idx]["item"] = load["item"]
                obj["loads"][idx]["volume"] = load["volume"]
                obj["loads"][idx]["creation_date"] = load["creation_date"]
        return True, json.dumps({property:obj[property]})
    else:
        return False, None

def GetAllFromDb(tablename:str) -> str:
    query = client.query(kind=tablename)
    q_limit = max(int(request.args.get('limit', '3')),3)
    q_offset = int(request.args.get('offset', '0'))
    l_iterator = query.fetch(limit= q_limit, offset=q_offset)
    pages = l_iterator.pages
    results = list(next(pages))
    if l_iterator.next_page_token:
        next_offset = q_offset + q_limit
        next_url = getpaginationurl(baseurl, tablename, q_limit, next_offset)
    else:
        next_url = None
    for e in results:
        e["id"] = e.key.id
        e["self"] = geturl(e.key.id, tablename)

    output = {f"{tablename}": results}
    if next_url:
        output["next"] = next_url
    return json.dumps(output)
             
def DeleteFromDb(id: str, tablename:str) -> bool:
    key = client.key(tablename, int(id))
    entity = client.get(key=key)
    if entity:
        if tablename == boatstablename: 
            SetLoadCarrierToNoneForBoatDeletion(entity)
        elif tablename == loadtablename:
            RemoveLoadFromBoat(entity)
        client.delete(key)
        return True
    else:
        return False


def RemoveLoadFromBoat(load):
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

# for loads in boat --> set carrier to None 
def SetLoadCarrierToNoneForBoatDeletion(boat):
    for loadRef in boat["loads"]:
        loadId = loadRef["id"]
        key = client.key(loadtablename, int(loadId))
        load = client.get(key=key)
        if load:
            load.update({"carrier" : None})
            client.put(load)
    
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

'''      
def EditBoatFromDb(boatId,boatData) -> Tuple[bool, bool, str]:
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
'''