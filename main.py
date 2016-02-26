import os
import json
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta, date
from datetools import date_to_dict
from google.appengine.api import users
import pytz
from models import Event, Track, Talk

app = Flask(__name__)


def process_event(event_file, user):
    event_data = json.loads(event_file)
    event_name = event_data['name']
    event_place = event_data['place']
    event_date_from = datetime.strptime(event_data['date_from'], '%Y-%m-%d').date()
    event_date_to = datetime.strptime(event_data['date_to'], '%Y-%m-%d').date()
    event_timezone = event_data['timezone']
    if 'description' in event_data:
        event_description = event_data['description']
    else:
        event_description = ''

    ev = Event(owner=user,
               name=event_name,
               place=event_place,
               date_from=event_date_from,
               date_to=event_date_to,
               timezone=event_timezone,
               description=event_description
               )
    ev.put()

    for track in event_data['tracks']:
        track_name = track['name']
        track_room = track['room']
        tr = Track(owner=user,
                   name=track_name,
                   room=track_room,
                   event=ev.key)
        tr.put()

        for talk in track['talks']:
            talk_title = talk['title']
            talk_authors = talk['authors']
            talk_start = datetime.strptime(talk['start'], '%Y-%m-%d %H:%M')
            talk_end = datetime.strptime(talk['end'], '%Y-%m-%d %H:%M')
            if 'tags' in talk:
                talk_tags = talk['tags']
            else:
                talk_tags = []

            if 'abstract' in talk:
                talk_abstract = talk['abstract']
            else:
                talk_abstract = ''

            tk = Talk(owner=user,
                      track=tr.key,
                      title=talk_title,
                      authors=talk_authors,
                      start=talk_start,
                      end=talk_end,
                      tags=talk_tags,
                      abstract=talk_abstract
                      )

            tk.put()


# All routes go to this file.
@app.route('/')
def hello():
    user = users.get_current_user()
    if user:
        return render_template('main.html', user=user, logout=users.create_logout_url('/'))
    else:
        return render_template('main.html', login=users.create_login_url('/panel'))


@app.route('/panel')
def control_panel():
    user = users.get_current_user()
    if user:
        events = Event.user_events(user)
        return render_template('panel.html', user=user, logout=users.create_logout_url('/'), events=events)
    else:
        return render_template('page_not_found.html'), 404


@app.route('/panel/new_event', methods=('GET', 'POST'))
def new_event():
    user = users.get_current_user()
    if request.method == 'GET':
        if user:
            return render_template('new_event.html')
        else:
            return render_template('page_not_found.html')

    elif request.method == 'POST':
        if user:
            return redirect('/panel')
        else:
            return redirect('/')


@app.route('/panel/upload_event', methods=('GET', 'POST'))
def upload_event():
    user = users.get_current_user()
    if request.method == 'GET':
        if user:
            return render_template('upload_event.html')
        else:
            return render_template('page_not_found.html')

    elif request.method == 'POST':
        if user:
            process_event(request.files['event_file'].read(), user)
            return redirect('/panel')
        else:
            return redirect('/')


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
