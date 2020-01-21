import time
import hashlib


def gen_password():
    return hashlib.md5(str(time.time()).encode()).hexdigest()
