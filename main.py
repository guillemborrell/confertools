import os
import json
from flask import Flask, render_template
from datetime import datetime, timedelta
from datetools import date_to_dict, timezones

app = Flask(__name__)

# All routes go to this file.
@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/time/<timezone>')
def clock(timezone):
    try:
        conference_time = datetime.utcnow(timezones[timezone])
    except KeyError:
        conference_time = datetime.utcnow()

    return json.dumps(date_to_dict(conference_time))

@app.route('/schedule/<schedule_id>')
def schedule(schedule_id):
    test_schedule = [
        {'event': 'first',
         'starts': date_to_dict(datetime.utcnow() + timedelta(minutes=1)),
         'finishes': date_to_dict(datetime.utcnow() + timedelta(minutes=4))},
        {'event': 'second',
         'starts': date_to_dict(datetime.utcnow() + timedelta(minutes=5)),
         'finishes': date_to_dict(datetime.utcnow() + timedelta(minutes=7))},
    ]
    return json.dumps(test_schedule)

@app.route('/<folder>/<file>')
def serve_static(folder, file):
    with open(os.path.join(os.curdir, 'static', folder, file)) as f:
        return f.read()

if __name__ == '__main__':
    app.debug = True
    app.run()
