import itertools

digits = '123456789'
print sum(int(''.join(perm)) for perm in itertools.permutations(digits))
