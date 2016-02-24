from google.appengine.ext import ndb


class Event(ndb.Model):
    owner = ndb.UserProperty(required=True)
    name = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    place = ndb.StringProperty(required=True)
    date_from = ndb.DateProperty(required=True)
    date_to = ndb.DateProperty(required=True)

    description = ndb.TextProperty()

class Track(ndb.Model):
    event = ndb.KeyProperty(required=True, kind=Event)
    name = ndb.StringProperty(required=True)