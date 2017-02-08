from google.appengine.ext import db
class MessageTable(db.Model):
    statusMessage=db.StringProperty()
    date= db.DateTimeProperty(auto_now=True)
    user=db.UserProperty()

class ScoreHistory(db.Model):
    wins=db.IntegerProperty()
    losses=db.IntegerProperty()
    user=db.UserProperty()
    
