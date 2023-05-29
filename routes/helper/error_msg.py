import json

errorMissingAttribute = {"Error" : "The request object is missing at least one of the required attributes"}
errorMissingBoat = {"Error" : "No boat with this boat_id exists"}
errorMissingLoad = {"Error" : "No load with this load_id exists"}
errorMissingOne = {"Error" : "The specified boat and/or load does not exist"}
errorLoadOnBoat = {"Error": "The load is already loaded on another boat"}
errorBoatLoad = {"Error": "No boat with this boat_id is loaded with the load with this load_id"}

errorMessage = {
    400 : {"Error" : "The request is missing at least one required attribute"},
    403 : {"Error" : "Boat does not belong to JWT owner"},
    404 : {"Error" : "No boat with this boat_id exists"},
    405 : {"Error" : "Method not supported at this address"},
    406 : {"Error" : "Unsupported Accept Header"},
}
