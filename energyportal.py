# -*- coding: utf-8 -*-
from flask import Flask, request, json

from db import insert_datapoint, insert_datapoints, create_db

app = Flask(__name__)
create_db()


@app.route('/input', methods=['POST'])
def post():
    data = json.loads(request.data)
    if isinstance(data, dict):
        insert_datapoint(**data)
    elif isinstance(data, list):
        insert_datapoints(data)

    return "OK", 201


if __name__ == '__main__':
    app.run()
