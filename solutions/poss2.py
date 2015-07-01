import itertools

digits = map(str, xrange(1, 10))
s = 0
for perm in itertools.permutations(digits):
	num = int(''.join(perm))
	print num
	s += num
print 'SUM', s
