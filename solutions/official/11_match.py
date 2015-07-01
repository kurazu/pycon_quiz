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
