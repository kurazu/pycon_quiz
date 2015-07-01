import math

DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
def convert(num, base):
    digits = []
    while num:
        num, rem = divmod(num, base)
        digit = DIGITS[rem]
        digits.append(digit)
    return ''.join(reversed(digits))

result = count('12456789abcdefghjklmnoprstuvwxyz', 36)
print convert(result, 36)
