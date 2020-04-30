from flask import Flask, request, g, Response
from flask_restful import Resource, Api
import json
from flask_jsonpify import jsonify
from gevent import pywsgi

import dgep

app = Flask(__name__)

@app.route("/<method>", methods=['GET','POST'])
@app.route("/<method>/<a>", methods=['GET','POST'])
@app.route("/<method>/<a>/<b>", methods=['GET','POST'])
def route_no_params(method, *args, **kwargs):
    if request.method == "POST":
        data = request.get_json()
    else:
        data = {}
    return dgep.handle(method, data, *args, **kwargs)

@dgep.interface
class RestInterface:
    def run(self):
        http_server = pywsgi.WSGIServer(('', 8888), app)
        http_server.serve_forever()
