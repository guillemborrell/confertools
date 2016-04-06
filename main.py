import json
import pytz
from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
from tools import date_to_dict
from google.appengine.api import users
from google.appengine.ext import ndb
from models import Event, Session, Talk
from tools import process_event
from timeline import timeline_from_event


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
        sessions_ = Session.in_event(event_key)
        return render_template('event.html',
                               event=event_,
                               sessions=[s for s in sessions_],
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
                           sessions=Session.in_event(event_key)
                           )


@app.route('/panel/session/<session_key>')
def session(session_key):
    user = users.get_current_user()
    if user:
        session_ = ndb.Key(urlsafe=session_key).get()
        return render_template('session.html',
                               session=session_,
                               talks=Talk.in_session(session_key),
                               user=user,
                               logout=users.create_logout_url('/')
                               )
    else:
        return render_template('page_not_found.html'), 404


@app.route('/session/<session_key>')
def public_session(session_key):
    session_ = ndb.Key(urlsafe=session_key).get()
    return render_template('public_session.html',
                           session=session_,
                           talks=Talk.in_session(session_key)
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


@app.route('/timing_data/<session_key>')
def timing_data(session_key):
    session_ = ndb.Key(urlsafe=session_key).get()
    event_ = session_.event.get()
    data = event_.data
    timeline = timeline_from_event(data, session_.name)
    print(timeline)
    return json.dumps(timeline)


@app.route('/timing/<session_key>')
def timing(session_key):
    session_ = ndb.Key(urlsafe=session_key).get()
    event_ = session_.event.get()

    return render_template('timing.html',
                           session=session_,
                           event=event_)


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
