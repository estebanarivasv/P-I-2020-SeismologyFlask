from flask import request, current_app
import requests
import json

# FINISH THIS SHIT UP
def getRequest(method, url, authenticated_user=False, data=None, id=None, form=None):
    headers = {
        "content-type": "application/json",
    }
    if authenticated_user:
        token = request.cookies['access_token']
        headers["authorization"] = "Bearer" + token

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

    if method == "PUT":
        r = requests.put(
            url=url,
            headers=headers,
            data=data)

    if method == "DELETE":
        r = requests.delete(
            url=url,
            headers=headers)

    return r
