#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import string
import math
from collections import Counter

NON_ALPHABET = re.compile('[^a-zA-Z]+')
ALPHABET = string.ascii_lowercase
FREQUENCY_ALPHABET = "etaoinshrdlcumwfgypbvkjxqz"
MODULE = len(ALPHABET)

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
