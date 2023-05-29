from typing import Tuple
from flask import Flask, request, jsonify, Blueprint, make_response, Response
from routes.helper.validation import errorMessage, errorMessageInputValidation

jsonmime = 'application/json'
htmlmime = 'text/html'

def validateId(id)-> Tuple[bool, dict]:
    '''
    Validate parameter id is of type int or can be converted to type int from string
    '''

    if not isinstance(id, int):
        try:
            int_value = int(id)
        except ValueError:
            return False, errorMessageInputValidation["id"]
        
    return True, None

def validateboatinputs(boatData, includeall: bool) -> Tuple[bool, str]:
    '''
    Validates boat for name, type, length 

    Returns T/F and error string
    '''
    # check for all required inputs
    if includeall and ("name" not in boatData or "type" not in boatData or "length" not in boatData):
        return False, errorMessage[400]
    
    # check for at least one required input
    checkOnce = ("name" in boatData or "type" in boatData or "length" in boatData)
    if not checkOnce: return False, errorMessage[400]

    # validation of each type if required
    if "name" in boatData and not validatestring(boatData["name"]): 
        return False, errorMessageInputValidation["name"]
    
    if "type" in boatData and not validatestring(boatData["type"]): 
        return False, errorMessageInputValidation["type"]
    
    if "length" in boatData and not validateint(boatData["length"]): 
        return False, errorMessageInputValidation["length"]
    
    return True, None

def validateloadinputs(loadData, includeall: bool) -> Tuple[bool, str]:
    '''
    Validates load for volume, item, creation_date 

    Returns T/F and error string
    '''
    # check for all required inputs
    if includeall and ("name" not in loadData or "type" not in loadData or "length" not in loadData):
        return False, errorMessage[400]
    
    # check for at least one required input
    checkOnce = ("name" in loadData or "type" in loadData or "length" in loadData)
    if not checkOnce: return False, errorMessage[400]

    # validation of each type if required
    if "name" in loadData and not validatestring(loadData["name"]): 
        return False, errorMessageInputValidation["name"]
    
    if "type" in loadData and not validatestring(loadData["type"]): 
        return False, errorMessageInputValidation["type"]
    
    if "length" in loadData and not validateint(loadData["length"]): 
        return False, errorMessageInputValidation["length"]
    
    return True, None

def validatestring(input) -> bool:
    '''
    Validate string has length 255 or fewer letters, length greater
    than zero, and starts and ends with a letter
    '''
    # is this type string?
    if type(input) != str:
        return False

    # length
    if len(input) > 255 or len(input) == 0:
        return False
    
    # lowercase, uppercase, spaces
    for c in input:
        if not (c.isupper() or c.islower() or c.isspace()):
            return False
        
    # start with letter
    if not input[0].isupper() and not input[0].islower():
        return False
    
    #end with letter
    if not input[-1].isupper() and not input[-1].islower():
        return False
        
    return True

def validateint(input):
    '''
    Validate input is an int
    '''
    # is this type int?
    if type(input) != int:
        return False

    return True

def validateMime(headeraccept: list[str], allowaccept: list[str]) -> bool:
    '''
    Validates Accept Headers
    '''
    for allow in allowaccept:
        if allow in headeraccept:
            return True
    return False