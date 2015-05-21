#!/bin/python
from random import random
import os
import subprocess
from flask import current_app
import psycopg2

path = os.path.dirname(os.path.realpath(__file__))


class entry:
    def __init__(self, value, weight=1):
        self.value = value
        self.weight = weight

    def __str__(self):
        return str(self.value)


def pick(entries):
    total_weight = sum(map(lambda entry: entry.weight, entries))
    choice_weight = total_weight*random()
    chosen = None
    i = 0

    while choice_weight > 0:
        chosen = entries[i]
        choice_weight -= chosen.weight
        i += 1

    chosen.weight /= 10

    for entry in entries:
        entry.weight += 1

    return chosen


def run():
    url_entries = []

    for file_name in filter(lambda x: x[-3:] == 'mp4', os.listdir(path)):
        url_entries.append(entry(path + '/' + file_name))

    dburi = current_app.config['SQLALCHEMY_DATABASE_URI']
    conn = psycopg2.connect(dburi)
    curs = conn.cursor()

    while True:
        next_video = pick(url_entries)
        curs.execute('NOTIFY queue;')
        subprocess.call(['ffmpeg', '-re', '-i', str(next_video), '-c', 'copy', '-f', 'flv', 'rtmp://localhost:1935/stream/live'])
