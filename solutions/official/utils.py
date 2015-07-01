from functools import wraps

def cached(func):
	cache = {}

	@wraps(func)
	def cached_wrapper(*args):
		if args not in cache:
			cache[args] = func(*args)
		return cache[args]

	return cached_wrapper
