import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return bool(USER_RE.match(username))


def valid_password(password):
    return bool(PW_RE.match(password))


def valid_email(email):
    return not email or bool(EMAIL_RE.match(email))

