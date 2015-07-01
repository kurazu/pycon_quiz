import itertools

digits = '2468'
print sum(int(''.join(perm)) for perm in itertools.permutations(digits))
