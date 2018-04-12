# -*- coding: utf-8 -*-
import sqlite3

import os
import time

db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       "energy.db")
conn = sqlite3.connect(db_file)


def create_db():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS datapoints
                 (timestamp INTEGER, 
                  kwh_high_total REAL, 
                  kwh_low_total REAL,
                  kw_current REAL,
                  gas_m3_total REAL)""")
    conn.commit()


def insert_datapoint(timestamp, kwh_high_total, kwh_low_total,
                     kw_current, gas_m3_total):
    c = conn.cursor()
    c.execute(
        "INSERT INTO datapoints VALUES ({0},{1},{2},{3},{4})".format(
            timestamp, kwh_high_total,kwh_low_total, kw_current, gas_m3_total))
    conn.commit()


def insert_datapoints(datapoints):
    for datapoint in datapoints:
        insert_datapoint(**datapoint)


def get_data_points(interval, points):
    now = time.time()
    c = conn.cursor()

    query = """
    SELECT MAX(timestamp),
           MAX(kwh_high_total), 
           MAX(kwh_low_total), 
           MAX(gas_m3_total), 
           SUM(kw_current) 
           FROM datapoints 
           WHERE timestamp > {0} AND timestamp <= {1};
    """

    periods = [
        (now, now - interval),
    ] + [
        (now - (interval * i), now - (interval * i+1))
        for i in range(1, points)
    ]

    ret = {}

    for p_end, p_start in periods:
        c.execute(query.format(p_start, p_end))
        conn.commit()
        result = c.fetchone()
        ret[result[0]] = {
            'kwh_high_total': result[1],
            'kwh_low_total': result[2],
            'gas_m3_total': result[3],
            'kw_current': result[4],
        }

    return ret
