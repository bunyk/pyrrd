import json
from subprocess import check_output, call
import sys
from time import time

from flask import Flask, request, send_file
app = Flask(__name__)

def get_file():
    try:
        return sys.argv[1]
    except IndexError:
        return None

def main():
    if not get_file():
        print('You should pass rrd file as first param')
        return
    app.run(debug=True)

@app.route("/")
def index():
    return send_file('index.html')

@app.route("/graph.png")
def graph():
    p = json.loads(request.args.get('params'))
    p['file'] = get_file()
    render_graph(**p)
    return send_file('graph.png')


def render_graph(**kwargs):
    print('params:', kwargs)
    t = int(kwargs['end'])
    interval = int(kwargs['interval'])
    call([
        'rrdtool',
        'graph',
        'graph.png',

        '--start=%s' % (t - interval),
        '--end=%s' % t,

        # set size of image
        '--width=%s' % kwargs['width'],
        '--height=%s' % kwargs['height'],
        '--full-size-mode',

        '--vertical-label=edits/min',
        'DEF:edits=%s:edits:AVERAGE' % kwargs['file'],
        'CDEF:editspermin=edits,60,*', # by default - per second
        'LINE2:editspermin%s:Wikipedia edit activity' % kwargs['color'],

        # return editspermin if it less then 2 else 0.
        'CDEF:low_activity=editspermin,2,LT,editspermin,0,IF',
        'AREA:low_activity#FF0000:"Low activity"', # draw area graph
    ])

if __name__ == "__main__":
    main()
