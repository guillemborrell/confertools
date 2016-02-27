from google.appengine.ext import ndb


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
    def tracks(cls):
        eid = cls.key.id()

        for track in Track.query(Track.event == ndb.Key(Event, eid)).order(-Track.created):
            yield track


class Track(ndb.Model):
    owner = ndb.UserProperty(required=True)
    event = ndb.KeyProperty(required=True, kind=Event)
    name = ndb.StringProperty(required=True)
    room = ndb.StringProperty(required=True)

    @classmethod
    def in_event(cls, event_key):
        for track in cls.query(
                Track.event == ndb.Key(urlsafe=event_key)):
            yield track


class Talk(ndb.Model):
    owner = ndb.UserProperty(required=True)
    track = ndb.KeyProperty(required=True, kind=Track)
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
                        Talk.track == ndb.Key(urlsafe=track_key)
                              ).order(-cls.start):
            yield talk


class Sponsor(ndb.Model):
    owner = ndb.UserProperty(required=True)
    name = ndb.StringProperty(required=True)
    level = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    logo = ndb.BlobProperty()