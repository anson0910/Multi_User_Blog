import logging
from google.appengine.ext import db

from utils.hashing_salt_functions import *
from utils.validate_info import *


class Post(db.Model):
    """
    Model for a blog post
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.StringProperty(required=True)


class User(db.Model):
    """
    Model for user
    """
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def get_by_name(cls, name):
        if not valid_username(name): return
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
        if valid_username(name):
            user = cls.get_by_name(name)
            if user and valid_pw(name, pw, user.pw_hash):
                return user

    @classmethod
    def print_to_log(cls):
        logging.info('printing database')
        q = db.GqlQuery('SELECT * FROM User')
        for u in q:
            logging.info(u.name + ' ' + u.pw_hash)

    @classmethod
    def delete_all(cls):
        db.delete(User.all())
