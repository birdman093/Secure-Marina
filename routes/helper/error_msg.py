import json
from credentials.names import *

def geterrormsg(tablename: str, statuscode: int):
    if tablename == loadtablename:
        return errorMessageLoad[statuscode]
    else:
        return errorMessageBoat[statuscode]

errorLoadOnBoat = {"Error": "Load is on a boat already"}
errorLoadNotOnOwnerBoat = {"Error": "The load is not on your boat and cannot be deleted"}

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



errorMessageInputValidationBoat = {
    "name" : {"Error" : "Invalid Name. Either No input, too long (more than 255 characters), contains invalid characters, or does not begin or end with a letter"},
    "type" : {"Error" : "Invalid Type. Either No input, too long (more than 255 characters), contains invalid characters, or does not begin or end with a letter"},
    "length" : {"Error" : "Invalid Length. Not an integer"},
    "id" : {"Error" : "Invalid id type"},
}

errorMessageInputValidationLoad = {
    "creation_date" : {"Error" : "Invalid Date. YYYY-MM-DD format required."},
    "item" : {"Error" : "Invalid Type. Either No input, too long (more than 255 characters), contains invalid characters, or does not begin or end with a letter"},
    "volume" : {"Error" : "Invalid Length. Not an integer"},
    "id" : {"Error" : "Invalid id type"},
}
