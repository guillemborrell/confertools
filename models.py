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
    sponsors = ndb.KeyProperty(repeated=True)


class Track(ndb.Model):
    owner = ndb.UserProperty(required=True)
    event = ndb.KeyProperty(required=True, kind=Event)
    name = ndb.StringProperty(required=True)


class Talk(ndb.Model):
    owner = ndb.UserProperty(required=True)
    track = ndb.KeyProperty(required=True, kind=Track)
    title = ndb.StringProperty(required=True)
    authors = ndb.StringProperty(required=True, repeated=True)
    start = ndb.DateTimeProperty(required=True)
    end = ndb.DateTimeProperty(required=True)
    room = ndb.StringProperty(required=True)
    tags = ndb.StringProperty(repeated=True)


class Sponsor(ndb.Model):
    owner = ndb.UserProperty(required=True)
    name = ndb.StringProperty(required=True)
    level = ndb.StringProperty(required=True)
    logo = ndb.BlobProperty()