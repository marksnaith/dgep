import requests
import json
import traceback

def call_uri(uri, data=None):
    if data is None:
        data = {}

    if type(data) is dict:
        data = json.dumps(data)

    try:
        result = requests.post(uri, data=data)
        response = result.json()
    except:
        response = {"response": False}
        traceback.print_exc()

    return response
