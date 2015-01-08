from subprocess import call
from time import time, sleep

from monitor_sources import get_wikipedia_edits

def create(filename, step=300, archives=((1, 288), (60, 720)), data=[]):
    if data:
        starttime = data[0][0] # start from the first data point timestamp
    else:
        starttime = int(time()) # start now
    RRA = ['RRA:AVERAGE:0.5:%s:%s' % a for a in archives]
    call([
        'rrdtool',
        'create',
        filename,
        '--step=%s' % step, 
        '--start=%s' % starttime,
        'DS:edits:COUNTER:600:U:U',
    ] + RRA)
    for t, value in data:
        print(t, value)
        update(filename, t, value)


def update(filename, t, value):
    call([
        'rrdtool',
        'update',
        filename,
        '%s:%s' % (t, value)
    ])


def create_again():
    with open('data.tsv') as f:
        data = [l.split() for l in f.readlines()]

    create('edits.rrd',
        step=60, # each minute
        archives=(
            (1, 1440), # each minute for a day
            (60, 720), # each 60 minutes for a 30 days
        ),
        data=data,
    )

def monitor():
    while True:
        value = get_wikipedia_edits()
        t = int(time())
        print(t, value)

        update('edits.rrd', t, value)

        sleep(60)

monitor()
