import io
from collections import defaultdict

count = 0
by_length = defaultdict(lambda: 0)

with io.open('/home/kurazu/workspace/pycon2013/CSW12.txt', 'r', encoding='utf-8') as input_:
	with io.open('/home/kurazu/workspace/pycon2013/scrabble.txt', 'w', encoding='utf-8') as output:
		lines = iter(input_)
		next(lines) # ignore description
		next(lines) # ignore empty row
		for row in lines:
			if not row:
				continue
			try:
				word, definition = row.split(u' ', 1)
			except ValueError:
				word = row.rstrip()
			output.write(word)
			output.write(u'\n')
			count += 1
			by_length[len(word)] += 1

print(u'{0} words written'.format(count))
for key in sorted(by_length.iterkeys()):
	print(u'{0}-letter words: {1}'.format(key, by_length[key]))
