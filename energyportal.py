# -*- coding: utf-8 -*-

from flask import Flask, json, make_response, render_template

import db

app = Flask(__name__)
db.create_db()


def calculate_usage(datapoints: dict):
    result = datapoints.copy()
    sorted_timestamps = sorted(datapoints)
    prev_timestamp = sorted_timestamps[0]

    for timestamp in sorted_timestamps:
        result[timestamp]['gas_used'] = (
                datapoints[timestamp]['gas_m3_total']
                - datapoints[prev_timestamp]['gas_m3_total']
        )

        prev_timestamp = timestamp

    return result


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/graph-data/<interval_secs>/<num_datapoints>", methods=["GET"])
def data_points(interval_secs, num_datapoints):
    ret = db.get_data_points(int(interval_secs), int(num_datapoints))
    enriched = calculate_usage(ret)

    response = make_response(json.dumps(enriched), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
