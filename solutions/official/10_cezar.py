LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TOTAL_LETTERS = len(LETTERS)
assert TOTAL_LETTERS == 26

def cezar(offset):
    alphabet = {letter: LETTERS[(i - offset) % TOTAL_LETTERS]
        for i, letter in enumerate(LETTERS)}
    def cipher(text):
        return ''.join(alphabet.get(char, char) for char in text)
    return cipher
