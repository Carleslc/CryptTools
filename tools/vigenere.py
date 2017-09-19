#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../lib")
from utils import *
from validator import *
import caesar
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

def crack(text, terminal=True):
    args.decrypt = True
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
    frequencies = most_frequent_chars(text)
    if args.verbose:
        print(f"Frequencies: {frequencies}")
    key_avg = friedman(text, frequencies)
    print(f"Friedman test suggests a key length of {key_avg}")
    # TODO Kasiki, Frequency analysis, Key extraction, Vigenere with key
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
