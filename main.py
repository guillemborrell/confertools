import json
import pytz
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
from tools import date_to_dict
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Event, Session, Talk
from tools import process_event

app = Flask(__name__)


# All routes go to this file.
@app.route('/')
def hello():
    user = users.get_current_user()
    events = Event.last_events()
    if user:
        return render_template('main.html',
                               user=user,
                               events=events,
                               logout=users.create_logout_url('/')
                               )
    else:
        return render_template('main.html',
                               events=events,
                               login=users.create_login_url('/panel')
                               )


@app.route('/panel')
def control_panel():
    user = users.get_current_user()
    if user:
        events = Event.user_events(user)
        return render_template('panel.html',
                               user=user,
                               logout=users.create_logout_url('/'),
                               events=events)
    else:
        return render_template('page_not_found.html'), 404


@app.route('/panel/event/<event_key>')
def event(event_key):
    user = users.get_current_user()
    if user:
        event_ = ndb.Key(urlsafe=event_key).get()
        return render_template('event.html',
                               event=event_,
                               tracks=Session.in_event(event_key),
                               user=user,
                               logout=users.create_logout_url('/')
                               )
    else:
        return render_template('page_not_found.html'), 404


@app.route('/event/<event_key>')
def public_event(event_key):
    event_ = ndb.Key(urlsafe=event_key).get()
    return render_template('public_event.html',
                           event=event_,
                           tracks=Session.in_event(event_key)
                           )


@app.route('/panel/session/<track_key>')
def track(track_key):
    user = users.get_current_user()
    if user:
        track_ = ndb.Key(urlsafe=track_key).get()
        return render_template('session.html',
                               track=track_,
                               talks=Talk.in_track(track_key),
                               user=user,
                               logout=users.create_logout_url('/')
                               )
    else:
        return render_template('page_not_found.html'), 404


@app.route('/session/<track_key>')
def public_track(track_key):
    track_ = ndb.Key(urlsafe=track_key).get()
    return render_template('public_track.html',
                           track=track_,
                           talks=Talk.in_track(track_key)
                           )


@app.route('/panel/talk/<talk_key>')
def talk(talk_key):
    user = users.get_current_user()
    if user:
        talk_ = ndb.Key(urlsafe=talk_key).get()
        return render_template('talk.html',
                               talk=talk_,
                               user=user,
                               logout=users.create_logout_url('/')
                               )
    else:
        return render_template('page_not_found.htm'), 404


@app.route('/talk/<talk_key>')
def public_talk(talk_key):
    talk_ = ndb.Key(urlsafe=talk_key).get()
    return render_template('public_talk.html', talk=talk_)


@app.route('/timing_data/<track_key>')
def timing_data(track_key):
    track_ = ndb.Key(urlsafe=track_key).get()
    event_ = track_.event.get()
    talks = Talk.in_track(track_.key.urlsafe())
    try:
        conference_time = datetime.now(pytz.timezone(event_.timezone))
    except KeyError:
        conference_time = datetime.utcnow()

    js_data = {'localtime': date_to_dict(conference_time),
               'event': event_.to_dict(),
               'session': track_.to_dict(),
               'talks': [t.to_dict() for t in talks]}

    return json.dumps(js_data)


@app.route('/timing/<track_key>')
def timing(track_key):
    track_ = ndb.Key(urlsafe=track_key).get()
    event_ = track_.event.get()
    return render_template('timing.html',
                           event=event_,
                           track=track_)


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


if __name__ == '__main__':
    app.debug = True
    app.run()
