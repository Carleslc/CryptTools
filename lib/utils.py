#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import string
import math
from collections import Counter
from functools import reduce

NON_ALPHABET = re.compile('[^a-zA-Z]+')
ALPHABET = string.ascii_lowercase
FREQUENCY_ALPHABET = "etaoinshrdlcumwfgypbvkjxqz"
MODULE = len(ALPHABET)
FAILED = (None, None)

def read(text=None):
    if not text:
        text = sys.stdin.read()
        if text[-1] == '\n':
            text = text[:-1]
    return text

def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(0)

def most_frequent_chars(text, size=MODULE):
    return Counter(NON_ALPHABET.sub('', text.lower())).most_common(size)

def most_frequent_char(text):
    return most_frequent_chars(text, size=1)[0][0]

def divisors(n):
    for i in range(1, math.ceil(n/2 + 1)):
        if n % i == 0: yield i
    yield n

def shift_by(char, shift):
    if char.isalpha():
        aux = ord(char) + shift
        z = 'z' if char.islower() else 'Z'
        if aux > ord(z):
            aux -= MODULE
        char = chr(aux)
    return char

def coincidence_index(text, frequencies=None):
    if frequencies is None:
        frequencies = most_frequent_chars(text)
    size = len(text)
    freq_sum = reduce(lambda x, y: x + y, map(lambda freq: freq[1]*(freq[1] - 1), frequencies))
    size_mult = size * (size - 1)
    return freq_sum / size_mult

def friedman(text, frequencies=None):
    kp = 0.067
    kr = 1/MODULE
    ko = coincidence_index(text, frequencies)
    return math.ceil((kp - kr)/(ko - kr))
