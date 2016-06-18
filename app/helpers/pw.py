import random
import string

from secret import SECRET
from lib.Crypto.Hash import SHA512


def gen_hash(pw, salt=None):
    if salt is None:
        salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in xrange(12))
    return SHA512.new(salt + SECRET + pw).hexdigest() + '|' + salt


def is_pw(pw, h):
    s = h.split('|')[1]
    return gen_hash(pw, s) == h
