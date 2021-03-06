import logging
from google.appengine.ext import db

from utils.hashing_salt_functions import *
from utils.validate_info import *


class User(db.Model):
    """
    Model for user
    """
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def get_by_name(cls, name):
        if not valid_username(name): return None
        q = db.GqlQuery("SELECT * FROM User WHERE name = '%s'" % name)
        return q.get()

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        user = User(name=name, pw_hash=pw_hash, email=email)
        user.put()
        return user

    @classmethod
    def login(cls, name, pw):
        user = cls.get_by_name(name)
        if user and valid_pw(name, pw, user.pw_hash):
            return user

    # @classmethod
    # def print_to_log(cls):
    #     logging.info('printing database')
    #     q = db.GqlQuery('SELECT * FROM User')
    #     for u in q:
    #         logging.info(u.name + ' ' + u.pw_hash)


class Post(db.Model):
    """
    Model for a blog post
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
    likes = db.IntegerProperty(default=0)
    users_liked = db.StringListProperty()   # list of user ids that like this post
    # can access an instance of Post's comments by typing instance_name.comments


class Comment(db.Model):
    """
    Model for a comment
    """
    post = db.ReferenceProperty(Post, collection_name='comments')
    content = db.TextProperty(required=True)
    created = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
