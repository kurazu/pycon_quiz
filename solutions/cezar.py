LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TOTAL_LETTERS = len(LETTERS)
assert TOTAL_LETTERS == 26

def cezar(offset):
	alphabet = {letter: LETTERS[(i + offset) % TOTAL_LETTERS] for i, letter in enumerate(LETTERS)}
	def cipher(text):
		return ''.join(alphabet[char] for char in text)
	return cipher

TEXT = 'CVRPRBSPNXR'
print('cezar0({0}) = {1}'.format(LETTERS, cezar(0)(LETTERS)))
print('cezar1({0}) = {1}'.format(LETTERS, cezar(1)(LETTERS)))
print('cezar13({0}) = {1}'.format(TEXT, cezar(13)(TEXT)))
print('cezar13(cezar13({0})) = {1}'.format(TEXT, cezar(13)(cezar(13)(TEXT))))


from functools import wraps

def cached(func):
	cache = {}

	@wraps(func)
	def cached_wrapper(*args):
		if args not in cache:
			cache[args] = func(*args)
		return cache[args]

	return cached_wrapper

@cached
def fib(n):
	if n == 1:
		return 1
	elif n == 2:
		return 2
	else:
		return fib(n - 2) + fib(n - 1)

print [fib(i) for i in xrange(1, 10)]

import io
import random

NUM_WORDS = 51
words = []
with io.open('scrabble.txt', 'r', encoding='utf-8') as file:
	for line in file:
		word = line.strip()
		if len(word) != 15:
			continue
		words.append(word)

selected_words = random.sample(words, NUM_WORDS)
selected_words, left = selected_words[:-1], selected_words[-1]

result = []
for selected_word in selected_words:
	result.append(selected_word)
	result.append(selected_word)
result.append(left)

random.shuffle(result)

e = []
for i, word in enumerate(result, 1):
	f = fib(i)
	encoder = cezar(f)
	encoded = encoder(word)
	print i, f, word, encoded
	e.append(encoded)

print '*' * 80
for i, w in enumerate(e, 1):
	print '<li><code>%s</code></li>' % w




