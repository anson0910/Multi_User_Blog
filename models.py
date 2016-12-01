from google.appengine.ext import db


class Post(db.Model):
    """
    Model for a blog post
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.StringProperty(required=True)
