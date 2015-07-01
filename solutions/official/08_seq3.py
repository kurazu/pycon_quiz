def cached(func):
	cache = {}
	def wrapper(arg):
		if arg not in cache:
			cache[arg] = func(arg)
		return cache[arg]
	return wrapper

@cached
def s(n):
	if n == 1:
		return 8
	if n == 2:
		return 9
	else:
		return s(n - 1) * 3 + s(n - 2) * 2

result = s(200)
print sum(int(digit) for digit in str(result))
