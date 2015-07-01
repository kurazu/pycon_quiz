import itertools

digits = '2', '4', '6', '8'
s = 0
for perm in itertools.permutations(digits):
	num = int(''.join(perm))
	print num
	s += num
print 'SUM', s

digits = '1', '2', '3', '4'
s = 0
for perm in itertools.permutations(digits):
	num = int(''.join(perm))
	print num
	s += num
print 'SUM', s
