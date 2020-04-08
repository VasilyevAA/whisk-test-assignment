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


def get_rnd_bool():
    return bool(random.getrandbits(1))


def generate_number(min=0, max=10, is_float=False, decimals=2):
    if is_float:
        return round(random.uniform(min, max), decimals)
    else:
        return random.randint(min, max)
