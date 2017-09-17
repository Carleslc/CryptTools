#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import enchant

NON_ALPHABET = re.compile('[^a-zA-Z]+')

class Validator:

    def __init__(self, lang='en_US', threshold=50, debug=False, beep=False):
        if threshold not in range(0, 101):
            error("threshold must be between 0 and 100")
        self.lang = lang
        self.percentage_success = threshold
        self.debug = debug
        self.beep = beep
        self.d = enchant.Dict(lang)

    def is_valid(self, text):
        """Checks if relevant words in `text` are written in `lang`"""
        words = NON_ALPHABET.split(text)
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
                valid = self.d.check(testWord)
                if self.debug:
                    validation = f"{testWord}: {valid}"
                    sys.stdout.write(validation)
                    sys.stdout.write(f"{' '*(25 - len(validation))}|\t")
                if valid:
                    i += 1
            progress = round(100 * (i/total))
            if self.debug and length > 1:
                sys.stdout.write(f"Progress {progress}%\t\t|\t")
            if length > 1 and progress >= self.percentage_success:
                return True
            max_progress = round(100 * ((i + total - count)/total))
            if self.debug and length > 1:
                sys.stdout.write(f"Max {max_progress}%")
                sys.stdout.write("\n")
            if max_progress < self.percentage_success:
                return False
        return False

    def success(self):
        print("SUCCESS")
        if self.beep:
            for i in range(3):
                os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 600))

    def fail(self):
        print(f"Sorry. None of decrypted results seems to be written in language {self.lang}...")
        if self.beep:
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 300))
