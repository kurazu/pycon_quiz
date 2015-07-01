DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'

"""
36
3, 6
0, 3
[6, 3]

80
8, 0
0, 8
"""

def convert(num, base):
	digits = []
	while num:
		num, rem = divmod(num, base)
		digit = DIGITS[rem]
		digits.append(digit)
	return ''.join(reversed(digits))

print convert(200, 16)
import pdb; pdb.set_trace()
