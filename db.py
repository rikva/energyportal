# -*- coding: utf-8 -*-
import sqlite3

import os
import time

db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       "energy.db")

GAS_PRICE_M3 = 0.66365
KWH_PRICE_HIGH_RATE = 0.21758
KWH_PRICE_LOW_RATE = 0.20539


def create_db():
    conn = sqlite3.connect(db_file)
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
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(
        "INSERT INTO datapoints VALUES ({0},{1},{2},{3},{4})".format(
            timestamp, kwh_high_total, kwh_low_total, kw_current, gas_m3_total))
    conn.commit()


def insert_datapoints(datapoints):
    for datapoint in datapoints:
        insert_datapoint(**datapoint)


def get_data_points(interval, points):
    now = time.time()
    conn = sqlite3.connect(db_file)
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
        (now - (interval * i), now - (interval * (i+1)))
        for i in range(1, points)
    ]

    ret = {}

    result = None
    power_cost = 0
    gas_cost = 0
    gas_usage = 0
    power_usage = 0

    for p_end, p_start in periods:
        c.execute(query.format(p_start, p_end))
        conn.commit()
        prev_result = result
        result = c.fetchone()

        if result and prev_result:
            high_rate_power_usage = (prev_result[1] - result[1])
            low_rate_power_usage = (prev_result[2] - result[2])
            power_usage = high_rate_power_usage + low_rate_power_usage

            gas_usage = prev_result[3] - result[3]

            high_rate_power_cost = high_rate_power_usage * KWH_PRICE_HIGH_RATE
            low_rate_power_cost = low_rate_power_usage * KWH_PRICE_LOW_RATE
            gas_cost = gas_usage * GAS_PRICE_M3

            power_cost = high_rate_power_cost + low_rate_power_cost

        try:
            ret[int(float(result[0]))] = {
                'kwh_high_total': result[1],
                'kwh_low_total': result[2],
                'gas_m3_total': result[3],
                'kw_current': result[4],
                'gas_usage': gas_usage,
                'gas_cost': gas_cost,
                'power_usage': power_usage,
                'power_cost': power_cost,
            }
        except TypeError:
            # timestamp was None
            continue

    return ret
