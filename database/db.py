from flask import request
from credentials.names import boatstablename, loadtablename, baseurl
from routes.helper.pagination import *
from google.cloud import datastore
import json

client = datastore.Client()

def GetAllFromDb_Pagination(tablename:str, owner: str) -> str:
    '''
    Get all from DB that match owner id, if owner == "" then no filter
    '''

    query = client.query(kind=tablename)
    if owner != "":
        query.add_filter('owner', '=', owner)
    q_limit = min(20,max(int(request.args.get('limit', '5')),5))
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

    # Query for total count
    count_query = client.aggregation_query(query).count() 
    count_result = count_query.fetch() 
    total = 0
    for aggregation_results in count_result:
        for aggregation in aggregation_results:
            total += aggregation.value

    output["total"] = total
    if next_url:
        output["next"] = next_url
    return json.dumps(output)