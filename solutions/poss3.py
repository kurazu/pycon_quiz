import itertools
import math

"""
123

123
132
213
231
312
321

1234

1234
1243
1324
1342
1423
1432
2134
2143
2314
2341
2413
2431
3124
3142
3214
3241
3412
3421
4123
4132
4213
4231
4312
4321

C = (l - 1)! * sum(digits)
C * b^(l - 1) + C * b^(l - 2) + C * b^(l - 3) + C * b^(l - 4)

C * 1 + C * b + C * b * b + C * b * b * b
C * (1 + b + b * b + b * b * b)
C * (1111)

"""
import math

def count(digits, base=10):
	l = len(digits)
	one = int('1' * l, base)
	digits = (int(d, base) for d in digits)
	C = sum(digits) * math.factorial(l - 1)
	return C * one

print count('1234', 10)
print count('2468', 10)
print count('123456789', 10)
print count('123456789abcdef', 16)
print '%x' % count('123456789abcdef', 16)
print count('12456789abcdefghjklmnoprstuvwxyz', 36)
print '%x' % count('12456789abcdefghjklmnoprstuvwxyz', 36)

import sys; sys.exit(0)
digits = '123456789abcdef'
s = 0
i = 0
target = math.factorial(len(digits))
for perm in itertools.permutations(digits):
	inp = ''.join(perm)
	num = int(''.join(perm), base=16)
	#print inp, num
	s += num
	i += 1
	if i % 100000 == 0:
		print i, '/', target, '%.2f%%' % (float(i) / target * 100)
print 'SUM', s
