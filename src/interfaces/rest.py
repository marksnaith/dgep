from flask import Flask, request, g, Response
from flask_restful import Resource, Api
import json
from flask_jsonpify import jsonify
from gevent import pywsgi

import dgep

app = Flask(__name__)

@app.route("/dgep/<method>", methods=['GET','POST'])
@app.route("/dgep/<method>/<a>", methods=['GET','POST'])
@app.route("/dgep/<method>/<a>/<b>", methods=['GET','POST'])
def route_no_params(method, *args, **kwargs):
    if request.method == "POST":
        data = request.get_json(force=True)
    else:
        data = {}
    return Response(dgep.handle(method, data, *args, **kwargs), mimetype='application/json')

@dgep.interface
class RestInterface:
    def run(self):
        print("Running RESTful interface")
        http_server = pywsgi.WSGIServer(('', 8888), app)
        http_server.serve_forever()
