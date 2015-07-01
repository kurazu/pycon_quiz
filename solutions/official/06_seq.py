from utils import cached

@cached
def s(n):
    if n == 1:
        return 8
    if n == 2:
        return 9
    else:
        return s(n - 1) * 3 + s(n - 2) * 2

print s(5)
