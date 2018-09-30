# -*- coding: utf-8 -*-
import os
from flask import Flask, request, json, make_response

import db

app = Flask(__name__)
db.create_db()

auth_token = os.getenv('AUTH_TOKEN')


@app.route("/input", methods=["POST"])
def post():
    request_token = request.headers.get("Authorization")
    if request_token is None or request_token != auth_token:
        return "Unauthorized", 401

    data = json.loads(request.data)
    if isinstance(data, dict):
        db.insert_datapoint(**data)
    elif isinstance(data, list):
        db.insert_datapoints(data)

    return "OK", 201


@app.route("/graph-data/<interval_secs>/<num_datapoints>", methods=["GET"])
def data_points(interval_secs, num_datapoints):
    ret = db.get_data_points(int(interval_secs), int(num_datapoints))
    response = make_response(json.dumps(ret), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/graph-data/<metric>/<interval_secs>/<num_datapoints>",
           methods=["GET"])
def data_points_per_metric(metric, interval_secs, num_datapoints):
    returndata = []

    for timestamp, datadict in db.get_data_points(int(interval_secs),
                                                  int(num_datapoints)).items():
        point = dict()
        point['x'] = timestamp
        point['y'] = datadict[metric]
        returndata.append(point)

    return json.dumps(returndata), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
