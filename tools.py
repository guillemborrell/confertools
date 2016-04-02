import json
import pytz
from datetime import datetime
from models import Event, Session, Talk


def date_to_dict(date):
    return {'year': date.year,
            'month': date.month,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute,
            'second': date.second}


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
               description=event_description,
               data=event_data
               )
    ev.put()

    for session in event_data['sessions']:
        session_name = session['name']
        session_room = session['room']
        tr = Session(owner=user,
                     name=session_name,
                     room=session_room,
                     event=ev.key)
        tr.put()

        for talk in session['talks']:
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
                      session=tr.key,
                      title=talk_title,
                      authors=talk_authors,
                      start=talk_start,
                      end=talk_end,
                      tags=talk_tags,
                      abstract=talk_abstract
                      )

            tk.put()

            
