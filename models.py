from google.appengine.ext import ndb


def datetime_to_dict(date):
    return {'year': date.year,
            'month': date.month,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute,
            'second': date.second}


def date_to_dict(date):
    return {'year': date.year,
            'month': date.month,
            'day': date.day}


class Event(ndb.Model):
    owner = ndb.UserProperty(required=True)
    name = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    place = ndb.StringProperty(required=True)
    date_from = ndb.DateProperty(required=True)
    date_to = ndb.DateProperty(required=True)
    timezone = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    data = ndb.JsonProperty()

    @classmethod
    def user_events(cls, user):
        for event in cls.query(Event.owner == user).order(-cls.created):
            yield event

    @classmethod
    def last_events(cls):
        for event in cls.query().order(-cls.created).fetch(10):
            yield event

    @classmethod
    def sessions(cls):
        eid = cls.key.id()

        for session in Session.query(Session.event == ndb.Key(Event, eid)).order(-Session.created):
            yield session

    def to_dict(self):
        return {
            'name': self.name,
            'created': datetime_to_dict(self.created),
            'modified': datetime_to_dict(self.modified),
            'place': self.place,
            'date_from': date_to_dict(self.date_from),
            'date_to': date_to_dict(self.date_to),
            'timezone': self.timezone,
            'data': self.data
            }


class Session(ndb.Model):
    owner = ndb.UserProperty(required=True)
    event = ndb.KeyProperty(required=True, kind=Event)
    name = ndb.StringProperty(required=True)
    track = ndb.StringProperty(required=True)
    room = ndb.StringProperty(required=True)

    @classmethod
    def in_event(cls, event_key):
        for session in cls.query(
                Session.event == ndb.Key(urlsafe=event_key)):
            yield session

    def to_dict(self):
        return {
            'name': self.name,
            'room': self.room
        }


class Talk(ndb.Model):
    owner = ndb.UserProperty(required=True)
    session = ndb.KeyProperty(required=True, kind=Session)
    title = ndb.StringProperty(required=True)
    authors = ndb.StringProperty(repeated=True)
    start = ndb.DateTimeProperty(required=True)
    end = ndb.DateTimeProperty(required=True)
    abstract = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    data = ndb.JsonProperty()

    @classmethod
    def in_track(cls, track_key):
        for talk in cls.query(
                        Talk.session == ndb.Key(urlsafe=track_key)
                              ).order(-cls.start):
            yield talk

    def to_dict(self):
        return {
            'title': self.title,
            'authors': self.authors,
            'start': datetime_to_dict(self.start),
            'end': datetime_to_dict(self.end),
        }


class Sponsor(ndb.Model):
    owner = ndb.UserProperty(required=True)
    name = ndb.StringProperty(required=True)
    level = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    logo = ndb.BlobProperty()