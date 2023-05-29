from typing import Tuple
from flask import Flask, render_template, request, jsonify
from google.cloud import datastore
import json
from credentials.names import boatstablename, loadtablename, baseurl
from routes.helper.pagination import *

client = datastore.Client()
    
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