import hashlib
import io

ENC = 'sha1$bh9ul$8e808fcea5418aa971311ea1598df65627ea3b98'
_, SALT, PWD = ENC.split('$')

def check(possibility):
	possibility = possibility.encode('utf-8')
	return hashlib.sha1(SALT + possibility).hexdigest() == PWD

with io.open('scrabble.txt', 'r', encoding='utf-8') as words:
	for word in words:
		word = word.rstrip()
		if not word:
			continue
		if check(word.lower()):
			print(u'DECODED {0}'.format(word))
			break
	else:
		print(u'Solution not found')
