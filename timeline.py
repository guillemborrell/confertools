import pytz
from datetime import datetime
import time


def timeline_from_event(event, session_name):
    name = event["name"]
    timezone = event["timezone"]
    localtime = pytz.timezone(timezone)
    utc = pytz.utc
    now = utc.localize(datetime.utcnow())
    boundaries = []
    
    for session in event['sessions']:
        if session["name"] == session_name:
            for talk in session['talks']:
                talk_start = localtime.localize(datetime.strptime(talk['start'],'%Y-%m-%d %H:%M'))
                talk_end = localtime.localize(datetime.strptime(talk['end'],'%Y-%m-%d %H:%M'))
            
                boundaries.append(
                    {"title": talk['title'],
                     "authors": talk['authors'],
                     "start": round((talk_start-now).total_seconds()),
                     "end": round((talk_end-now).total_seconds()),
                     "warning": talk['warning'],
                     'questions': talk['questions'],
                     'transition': talk['transition']
                     }
                )

    # Now I got the boundaries of the event.
    # Construct the complete timeline with the status of
    # the panel every second.
    status = []
    
    if boundaries[0]['start'] > 0:
        running = False
        finished = False
    elif boundaries[-1]['end'] < 0:
        running = False
        finished = True
    elif boundaries[0]['start'] < 0 < boundaries[-1]['end']:
        running = True
        finished = False

    if not finished:
        if not running:
            b = boundaries[0]
            print('Event not started yet')
            print('Event starts at {}'.format(b['start']))

            status.append(
                {'time':0,
                 'panel': 'black',
                 'title': b['title'],
                 'authors': b['authors'],
                }
            )
        for b in boundaries:
            remaining_time = 60*(b['transition'])
            elapsed = b['start'] - remaining_time
            if elapsed > 0:
                status.append(
                    {'time': elapsed,
                     'panel': 'black',
                     'title': b['title'],
                     'authors': b['authors']
                    }
                )    
            elapsed = b['start']
            if elapsed > 0:
                status.append(
                    {'time': elapsed,
                     'panel': 'green',
                     'title': b['title'],
                     'authors': b['authors'],
                    }
                )
            remaining_time = 60*(b['warning']+b['questions'])
            elapsed = b['end'] - remaining_time
            if elapsed > 0:
                status.append(
                    {'time': elapsed,
                     'panel': 'yellow',
                     'title': b['title'],
                     'authors': b['authors']
                    }
                )
            remaining_time = 60*(b['questions'])
            elapsed = b['end'] - remaining_time
            if elapsed > 0:
                status.append(
                    {'time': elapsed,
                     'panel': 'red',
                     'title': b['title'],
                     'authors': b['authors']
                    }
                )
            
    status.append(
        {'time': round(1E6),
         'panel': 'black',
         'title': 'The event is over',
         'authors': ''
         }
    )

    return status


def test_timeline_from_event():
    event = {
        "name": "Test Event",
        "date_from": "2016-02-26",
        "date_to": "2016-02-29",
        "timezone": "Europe/Madrid",
        "description": "A test event",
        "place": "Somewhere",
        "sessions": [
            {
                "name": "A session",
                "room": "Room 01",
                "talks": [
                    {
                        "title": "A test talk 1",
                        "authors": ["Me author", "You author"],
                        "start" : "2016-04-2 18:30",
                        "end" : "2016-04-2 18:50",
                        "warning": 5,
                        "questions": 5,
                        "transition": 5
                    },
                    {
                        "title": "A test talk 2",
                        "authors": ["Me author", "You author"],
                        "start" : "2016-04-2 18:50",
                        "end" : "2016-04-2 19:20",
                        "warning": 5,
                        "questions": 5,
                        "transition": 5
                    }
                ]}
        ]}
    localtime = pytz.timezone(event['timezone'])

    print(timeline_from_event(event, "A session"))


if __name__ == '__main__':
    test_timeline_from_event()
