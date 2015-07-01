import math

def count(digits, base=10):
    l = len(digits)
    one = int('1' * l, base)
    digits = (int(d, base) for d in digits)
    C = sum(digits) * math.factorial(l - 1)
    return C * one

print '%x' % count('123456789abcdef', 16)
