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

def flatmap(f, items):
    return [x for mappedList in map(f, items) for x in mappedList]

def flatten(listOfLists):
    return flatmap(lambda l: l, listOfLists)

def repetitions(l):
    result = Counter(l).most_common(len(l))
    def comparator(x):
        return -x[1], x[0]
    result.sort(key=comparator)
    return result

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

def find_sequence_duplicates(text, min_length=3):
    text = NON_ALPHABET.sub('', text.lower())

    sizeAlpha = len(text) + 1
    seqSpacings = {}

    lengths = [[0] * i for i in range(sizeAlpha)]

    for i in range(1, sizeAlpha):
        if args.verbose:
            sys.stdout.write("\r")
            sys.stdout.write(f"{round(100 * (i/(sizeAlpha- 1)))}% ")
            sys.stdout.flush()
        for j in range(1, i):
            if text[i - 1] == text[j - 1]:
                duplicate_length = lengths[i][j] = lengths[i - 1][j - 1] + 1
                spacing = i - j
                if duplicate_length >= min_length and (i >= (sizeAlpha - 1) or text[i] != text[j]):
                    duplication = text[i - duplicate_length:i]
                    if duplication not in seqSpacings:
                        seqSpacings[duplication] = []
                    seqSpacings[duplication].append(spacing)
    if args.verbose:
        print()
    return seqSpacings
