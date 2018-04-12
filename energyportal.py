# -*- coding: utf-8 -*-
import os
from flask import Flask, request, json

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


@app.route("/graph-data/<interval>/<datapoints>", methods=["GET"])
def get_last_hour(interval, datapoints):
    electricity = []

    for timestamp, datadict in db.get_data_points(int(interval),
                                                  int(datapoints)).items():
        point = dict()
        point['x'] = timestamp
        point['y'] = datadict['kw_current']
        electricity.append(point)

    return json.dumps(electricity), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
