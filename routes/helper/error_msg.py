import json
from credentials.names import *

def geterrormsg(statuscode: int, tablename: str):
    if tablename == loadtablename:
        return errorMessageLoad[statuscode]
    else:
        return errorMessageBoat[statuscode]

errorMissingAttribute = {"Error" : "The request object is missing at least one of the required attributes"}
errorMissingBoat = {"Error" : "No boat with this boat_id exists"}
errorMissingLoad = {"Error" : "No load with this load_id exists"}
errorMissingOne = {"Error" : "The specified boat and/or load does not exist"}
errorLoadOnBoat = {"Error": "The load is already loaded on another boat"}
errorBoatLoad = {"Error": "No boat with this boat_id is loaded with the load with this load_id"}

errorMessageBoat = {
    400 : {"Error" : "The request is missing at least one required attribute"},
    403 : {"Error" : "Boat does not belong to JWT owner"},
    404 : {"Error" : "No boat with this boat_id exists"},
    405 : {"Error" : "Method not supported at this address"},
    406 : {"Error" : "Unsupported Accept Header"},
}

errorMessageLoad = {
    400 : {"Error" : "The request is missing at least one required attribute"},
    403 : {"Error" : "Boat does not belong to JWT owner"},
    404 : {"Error" : "No load with this load_id exists"},
    405 : {"Error" : "Method not supported at this address"},
    406 : {"Error" : "Unsupported Accept Header"},
}



errorMessageInputValidation = {
    "name" : {"Error" : "Invalid Name. Either No input, too long (more than 255 characters), contains invalid characters, or does not begin or end with a letter"},
    "type" : {"Error" : "Invalid Type. Either No input, too long (more than 255 characters), contains invalid characters, or does not begin or end with a letter"},
    "length" : {"Error" : "Invalid Length. Not an integer"},
    "id" : {"Error" : "Invalid id type"},
}
