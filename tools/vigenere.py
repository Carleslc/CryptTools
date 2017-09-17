#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../lib")
from utils import *
from validator import *
import enchant
import argparse

def vigenere(text, key):
    result = ""
    shifts = [ord(k) - ord('a') for k in key.lower()]
    if args.verbose:
        print(f'Key "{key}" shifts: {shifts}')
    i = 0
    key_length = len(key)
    def do_shift(char):
        nonlocal i
        if char.isalpha():
            shift = shifts[i] if not args.decrypt else MODULE - shifts[i]
            shifted = shift_by(char, shift)
            i = i + 1 if i + 1 < key_length else 0
            return shifted
        return char
    return ''.join(map(do_shift, text))

parser = argparse.ArgumentParser()
parser.add_argument("key", help="key used to encrypt or decrypt")
parser.add_argument("-t", "--text", help="text to read from. If not specified the program will read from standard input")
parser.add_argument("--decrypt", action='store_true', help="use the key to decrypt the text")
parser.add_argument("-V", "--verbose", action='store_true', help="show extra information")
args = parser.parse_args()

#validator = Validator(args.lang, args.threshold, args.debug, args.beep)
text = read(args.text)
size = len(text)

if not args.key.isalpha():
    error("key must be alphabetic and non-empty")

print(vigenere(text, args.key))
