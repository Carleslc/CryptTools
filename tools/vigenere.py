#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../lib")
from validator import *
from utils import FAILED, MODULE, flatten, flatmap, read
import utils
import caesar
import math
import enchant
import argparse

def set_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", help="text to read from. If not specified the program will read from standard input")
    parser.add_argument("-k", "--key", help="key used to encrypt or decrypt. If no key is provided the program will try to crack and decrypt using the specified language")
    parser.add_argument("--decrypt", action='store_true', help="use the key to decrypt the text")
    parser.add_argument("-l", "--lang", help=f"available languages: {enchant.list_languages()} (default: en_US). Only useful if no key is provided", default='en_US')
    parser.add_argument("-V", "--verbose", action='store_true', help="show extra information")
    parser.add_argument("-A", "--all", action='store_true', help="show decrypted text for each tested key")
    parser.add_argument("-D", "--debug", action='store_true', help="show information about text validation")
    parser.add_argument("-T", "--threshold", help="valid word count percentage to mark the whole text as valid language (default: 50)", type=int, default=50)
    parser.add_argument("--beep", action='store_true', help="plays a beep sound when program finishes. May require SOX to be installed")
    args = parser.parse_args()

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

def useful_divisors(terms):
    return flatmap(lambda n: list(utils.divisors(n))[1:], terms)

def caesar_crack(text):
    if args.verbose:
        print("Testing key length 1 (Caesar crack)")
    caesar.args = args
    caesar.validator = validator
    (decryptedKey, decryptedText) = caesar.crack(text, terminal=False)
    if decryptedKey is not None:
        key = chr(decryptedKey + ord('A'))
        if terminal:
            if args.verbose:
                print(f"Key: {key}")
            print(decryptedText)
        return (key, decryptedKey)
    elif args.verbose:
        print("Caesar failed")
    return FAILED

def friedman(text, frequencies=None):
    kp = 0.067
    kr = 1/MODULE
    ko = utils.coincidence_index(text, frequencies)
    return math.ceil((kp - kr)/(ko - kr))

def kasiki(text):
    if args.verbose:
        print("Finding sequence duplicates and spacings...")
    utils.args = args
    min_length = 2 if len(text) < 100 else 3
    seqSpacings = utils.find_sequence_duplicates(text, min_length)
    if args.verbose:
        if args.all:
            print(seqSpacings)
        print("Extracting spacing divisors...")
    divisors = useful_divisors(flatten(list(seqSpacings.values())))
    divisorsCount = utils.repetitions(divisors)
    return [x[0] for x in divisorsCount]

def crack(text, terminal=True):
    args.decrypt = True
    tryCaesar = caesar_crack(text)
    if tryCaesar != FAILED:
        return tryCaesar
    frequencies = utils.most_frequent_chars(text)
    if args.all:
        print(f"Frequencies: {frequencies}")
    key_avg = friedman(text, frequencies)
    if args.verbose and key_avg > 0:
        print(f"Friedman test suggests a key length of {key_avg}")
        # TODO: Test key_avg
    if args.verbose:
        print("Kasiki examination")
    key_lengths = kasiki(text)
    if args.all:
        print("Kasiki possible key lengths (sorted by probability):")
        print(key_lengths)
    for key_length in key_lengths:
        if args.verbose:
            print(f"Testing key length of {key_length}")
        # TODO
    if terminal:
        validator.fail()
    return FAILED

if __name__ == "__main__":
    set_args()

    if args.key is not None and not args.key.isalpha():
        error("key must be alphabetic and non-empty")

    validator = Validator(args.lang, args.threshold, args.debug, args.beep)
    text = read(args.text)
    size = len(text)

    if args.key is not None:
        print(vigenere(text, args.key))
    else:
        crack(text)
