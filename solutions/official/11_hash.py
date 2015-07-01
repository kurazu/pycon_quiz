import hashlib

ENCODED = 'sha1$bh9ul$8e808fcea5418aa971311ea1598df65627ea3b98'
_, SALT, PASSWORD = ENCODED.split('$')

def check(possibility):
    return hashlib.sha1(SALT + possibility).hexdigest() == PASSWORD
