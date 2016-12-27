#/usr/bin/env/python
# coding=utf-8

import json
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

connection = sqlite3.connect('microbe.db')
connection.row_factory = dict_factory
cursor = connection.cursor()
cursor.execute("SELECT * FROM Microbe;")
python_db = cursor.fetchall()

json_db = json.dumps(python_db, ensure_ascii=False)

json_file = open('microbe_db.json', 'w')
json_file.write(json_db)
json_file.close()