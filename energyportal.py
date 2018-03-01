# -*- coding: utf-8 -*-
import os
from flask import Flask, request, json

from db import insert_datapoint, insert_datapoints, create_db

app = Flask(__name__)
create_db()

auth_token = os.getenv('AUTH_TOKEN')


@app.route("/input", methods=["POST"])
def post():
    request_token = request.headers.get("Authorization")
    if request_token is None or request_token != auth_token:
        return "Unauthorized", 401

    data = json.loads(request.data)
    if isinstance(data, dict):
        insert_datapoint(**data)
    elif isinstance(data, list):
        insert_datapoints(data)

    return "OK", 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
