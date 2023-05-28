errorMissingAttribute = {"Error" : "The request object is missing at least one of the required attributes"}
errorMissingBoat = {"Error" : "No boat with this boat_id exists"}
errorMissingLoad = {"Error" : "No load with this load_id exists"}
errorMissingOne = {"Error" : "The specified boat and/or load does not exist"}
errorLoadOnBoat = {"Error": "The load is already loaded on another boat"}
errorBoatLoad = {"Error": "No boat with this boat_id is loaded with the load with this load_id"}

local = "http://127.0.0.1:8080"
production = "https://intrestfulapi.ue.r.appspot.com"
baseurl = production

boatstablename = "boats"
loadtablename = "loads"

def geturl(id: str, tablename: str):
    return f"{baseurl}/{tablename}/{id}"

def getpaginationurl(base_url, tablename, q_limit, next_offset):
    return base_url + "/" + str(tablename) + "/?limit=" + str(q_limit) + "&offset=" + str(next_offset)