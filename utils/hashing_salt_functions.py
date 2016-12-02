import hashlib
import hmac
import random
import string

from secret import SECRET


def make_secure_val(s):
    """returns a string of the format s|hash(s)"""
    def hash_str(s):
        """Hashes given string str and returns result"""
        return hmac.new(SECRET, s).hexdigest()
    return s + '|' + hash_str(s)


def check_secure_val(h):
    """
    :param h: String of the format s|HASH
    :return: s if hash_str(s) == HASH, otherwise None
    """
    if not h: return None
    strs = h.split('|')
    if not strs or len(strs) != 2: return None
    s = strs[0]
    if make_secure_val(s) == h: return s


def make_salt():
    chars = string.letters  # + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(5))


def make_pw_hash(name, pw, salt=make_salt()):
    """
    :param name: username
    :param pw: user password
    :param salt: use salt if provided, otherwise generate random salt
    :return: string of the format HASH(name + pw + salt),salt
    """
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    """
    :param name: username
    :param pw: user password
    :param h: string of the format HASH(name + pw + salt),salt
    :return: True if a user's password matches its hash
    """
    if not name or not pw or not h: return False
    salt = h.split(',')[1]
    return make_pw_hash(name, pw, salt) == h
