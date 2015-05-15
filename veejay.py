#!/bin/python
from random import random
import os
import subprocess

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

url_entries = []

for file_name in filter(lambda x: x[-3:] == 'mp4', os.listdir('shitstream-files')):
    url_entries.append(entry('./shitstream-files/' + file_name))

while True:
    next_url = pick(url_entries)
    subprocess.call(['ffmpeg', '-re', '-i', str(next_url), '-c', 'copy', '-f', 'flv', 'rtmp://localhost:1935/stream/live']).wait()
