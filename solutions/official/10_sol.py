from collections import defaultdict

WORDS = ["TVCWPDBMJTBUJPO","..."]
decoded_words = defaultdict(lambda: 0)

for n, word in enumerate(WORDS, 1):
    offset = fib(n)
    cipher = cezar(offset)
    decoded_word = cipher(word)
    decoded_words[decoded_word] += 1

for decoded_word, count in decoded_words.iteritems():
    if count == 1:
        print decoded_word
