import os
import json
from flask import Flask, render_template
from datetime import datetime, timedelta
from datetools import date_to_dict, timezones
from google.appengine.api import users
import pytz

app = Flask(__name__)


# All routes go to this file.
@app.route('/')
def hello():
    user = users.get_current_user()
    if user:
        return render_template('main.html', user=user)
    else:
        return render_template('main.html', login=users.create_login_url('/panel'))


@app.route('/panel')
def control_panel():
    user = users.get_current_user()
    if user:
        return render_template('panel.html', user=user, logout=users.create_logout_url('/'))
    else:
        return render_template('page_not_found.html'), 404


@app.route('/time/UTC')
def utc_clock():
    conference_time = datetime.utcnow()
    return json.dumps(date_to_dict(conference_time))


@app.route('/time/<continent>/<city>')
def clock(continent, city):
    try:
        conference_time = datetime.now(pytz.timezone('/'.join([continent, city])))
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
