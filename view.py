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
        'DEF:edits=%s:edits:AVERAGE' % kwargs['file'],
        'LINE2:edits%s' % kwargs['color'],
    ])

if __name__ == "__main__":
    main()
