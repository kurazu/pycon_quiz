import hashlib

ENCODED = 'sha1$bh9ul$8e808fcea5418aa971311ea1598df65627ea3b98'
_, SALT, PASSWORD = ENCODED.split('$')

def check(possibility):
	return hashlib.sha1(SALT + possibility).hexdigest() == PASSWORD

f = open('solutions/official/CSW12.txt', 'rb')
for row in f:
	row = row.rstrip()
	if not row:
		continue
	if ' ' in row:
		word, _ = row.split(' ', 1)
	else:
		word = row
	if check(word.lower()):
		print(u'DECODED {0}'.format(word))
		break
else:
	print(u'Solution not found')

f.close()

