#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import numpy as np
import math
import enchant
import re

FILL_CHARACTER = ' '

def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(0)

def success():
    print("SUCCESS")
    if args.beep:
        for i in range(3):
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 600))

def fail():
    print(f"Sorry. None of decrypted results seems to be written in language {lang}...")
    if args.beep:
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 300))

def key_to_matrix_bounds(key):
    rows = key
    cols = math.ceil(size/rows)
    return (rows, cols)

def scytale(text, rows, cols):
    """Encrypts/Decrypts a `text` using the scytale transposition cipher with specified `key`"""
    m = np.array(list(text.ljust(rows*cols, FILL_CHARACTER))).reshape((rows, cols))
    result = ''.join([''.join(row) for row in m.transpose()]).strip()
    if args.all and args.key is not None:
        print(f'Text to cipher: "{text}" ({len(text)})')
        print(m)
        print(f"Result size: {len(result)}")
    return result

def cipher(text):
    bounds = key_to_matrix_bounds(args.key)
    rows = bounds[0]
    cols = bounds[1]
    if args.verbose:
        print(f"Testing matrix: {rows}x{cols}")
    return scytale(text, rows, cols)

def is_valid(text, lang='en_US'):
    """Checks if relevant words in `text` are written in `lang`"""
    if args.verbose and args.debug:
        print()
    words = re.split("[ \t\n\r-,.¡!¿?<>\/`´\"']+", text)
    total = len(words)
    count = 0
    i = 0
    for word in words:
        count += 1
        length = len(word)
        if length == 0:
            i += 1
        elif length > 1:
            testWord = word.lower()
            valid = d.check(testWord)
            if args.debug:
                validation = f"{testWord}: {valid}"
                sys.stdout.write(validation)
                sys.stdout.write(f"{' '*(25 - len(validation))}|\t")
            if valid:
                i += 1
        progress = round(100 * (i/total))
        if args.debug and length > 1:
            sys.stdout.write(f"Progress {progress}%\t\t|\t")
        if length > 1 and progress >= percentage_success:
            return True
        max_progress = round(100 * ((i + total - count)/total))
        if args.debug and length > 1:
            sys.stdout.write(f"Max {max_progress}%")
            sys.stdout.write("\n")
        if max_progress < percentage_success:
            return False
    return False

def test(text, rows, cols):
    decrypt = scytale(text, rows, cols)
    if args.verbose:
        sys.stdout.write("\r")
        sys.stdout.write(f"Testing matrix: {rows}x{cols}       ")
        sys.stdout.flush()
    if args.all:
        print(f'Testing decrypted text:\n"{decrypt}"')
    valid = is_valid(decrypt, lang)
    if args.debug:
        print()
    if valid:
        if args.verbose:
            success()
        print(decrypt)
        return True
    return False

def testKeys(text, keys):
    for k in keys:
        bounds = key_to_matrix_bounds(k)
        rows = bounds[0]
        cols = bounds[1]
        if test(text, rows, cols) or test(text, cols, rows):
            return True
    return False

def crack(text):
    """Cracks the text that must be encrypted with the scytale cipher"""
    if args.verbose:
        print(f'Text to crack: "{text}" ({size})')
    divs = list(divisors(size))
    keys = [x for x in range(2, size) if x not in divs]
    if testKeys(text, divs) or testKeys(text, keys):
        return
    fail()

def divisors(n):
    for i in range(1, math.ceil(n/2 + 1)):
        if n % i == 0: yield i

# MAIN

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--text", help="text to read from. If not specified the program will read from standard input")
parser.add_argument("-k", "--key", help="key used to encrypt. If no key is provided the program will try to crack and decrypt using the specified language", type=int)
parser.add_argument("-l", "--lang", help=f"available languages: {enchant.list_languages()} (default: en_US). Only useful if no key is provided")
parser.add_argument("-V", "--verbose", action='store_true', help="show extra information")
parser.add_argument("-A", "--all", action='store_true', help="show decrypted text for each tested key")
parser.add_argument("-D", "--debug", action='store_true', help="show information about text validation")
parser.add_argument("-T", "--threshold", help="valid word count percentage to mark the whole text as valid language (default: 50)", type=int)
parser.add_argument("--beep", action='store_true', help="plays a beep sound when program finishes. May require SOX to be installed")

args = parser.parse_args()
lang = args.lang
if not args.lang:
    lang = "en_US"
d = enchant.Dict(lang)
percentage_success = 50
if args.threshold:
    percentage_success = args.threshold
    if percentage_success not in range(0, 101):
        error("threshold must be between 0 and 100")
text = args.text
if not text:
    text = sys.stdin.read()
    if text[-1] == '\n':
        text = text[:-1]
size = len(text)
if args.key is not None:
    if args.key not in range(1, size + 1):
        error(f"key must be between 1 and {size}")
    print(cipher(text))
else:
    crack(text)
