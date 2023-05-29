from credentials.names import baseurl

def geturl(id: str, tablename: str):
    return f"{baseurl}/{tablename}/{id}"

def getpaginationurl(base_url, tablename, q_limit, next_offset):
    return base_url + "/" + str(tablename) + "/?limit=" + str(q_limit) + "&offset=" + str(next_offset)