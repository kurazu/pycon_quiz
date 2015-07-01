import math

DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
def convert(num, base):
	digits = []
	while num:
		num, rem = divmod(num, base)
		digit = DIGITS[rem]
		digits.append(digit)
	return ''.join(reversed(digits))

def count(digits, base=10):
	l = len(digits)
	one = int('1' * l, base)
	digits = (int(d, base) for d in digits)
	C = sum(digits) * math.factorial(l - 1)
	return C * one

result = count('12456789abcdefghjklmnoprstuvwxyz', 36)
print convert(result, 36)
