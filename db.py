# -*- coding: utf-8 -*-
import sqlite3

import os

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

