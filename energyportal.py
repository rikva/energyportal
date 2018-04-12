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


@app.route("/last-hour", methods=["GET"])
def get_last_hour():
    electricity = {}

    for timestamp, datadict in db.get_last_hour().items():
        electricity[timestamp] = datadict['kw_current']

    return json.dumps(electricity), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
