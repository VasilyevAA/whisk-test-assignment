import string
import random


def generate_value(size=10, chars=string.ascii_letters + string.digits, prefix='', suffix=''):
    """
    Can change on hypothesis or another generation libs, but its additional strong requirement
    """
    len_pref, len_suff = len(prefix), len(suffix)
    if len_pref + len_suff >= size:
        raise Exception("Can't generate random string. Long suffix or/and  prefix")
    size = size - len_pref - len_suff
    random_string = ''.join([prefix] + [random.choice(chars) for _ in range(size)] + [suffix])
    return random_string