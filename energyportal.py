# -*- coding: utf-8 -*-

from flask import Flask, json, make_response

import db

app = Flask(__name__)
db.create_db()


@app.route("/graph-data/<interval_secs>/<num_datapoints>", methods=["GET"])
def data_points(interval_secs, num_datapoints):
    ret = db.get_data_points(int(interval_secs), int(num_datapoints))
    response = make_response(json.dumps(ret), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
