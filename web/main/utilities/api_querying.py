from flask import request, current_app, redirect, url_for, flash
from werkzeug.routing import RequestRedirect
import requests
from json import dumps

def makeRequest(method, url, authenticated_user=False, data="{}"):
    
    headers = {
        "content-type": "application/json",
    }
    if authenticated_user:
        #Recolectamos el token de las cookies
        token = request.cookies['access_token']
        #Incorporamos el token en el headers
        headers["authorization"] = "Bearer " + token

    if method == "GET":
        r = requests.get(
            url=url,
            headers=headers,
            data=data)
        
    if method == "POST":
        r = requests.post(
            url=url,
            headers=headers,
            data=data)
        if r.status_code == 201:
            flash("Addition succesfully completed.", 'success')

    if method == "PUT":
        r = requests.put(
            url=url,
            headers=headers,
            data=data)
        if r.status_code == 201:
            flash("Modification succesfully completed.", 'success')

    if method == "DELETE":
        r = requests.delete(
            url=url,
            headers=headers)
        print(r.status_code)
        if r.status_code == 204:
            flash("Deletion succesfully completed.", 'success')
    
    if r.status_code == 401 or r.status_code == 422:
        flash("Authorization token not valid. Please log in again.", 'warning')
        raise RequestRedirect(url_for('auth.logout'))


    # RETURNS A JSON (STR TYPE)
    return r

