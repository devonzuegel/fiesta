# -*- coding: utf-8 -*-

import sys
import getopt
import os
import math
import collections
import copy
import re
from datetime import datetime
from bisect import bisect_left
import numpy as np
from IBMModel1 import M1
import nltk

UTF_SPECIAL_CHARS = {
  '\\xc2\\xa1' : '',
  '\\xc2\\xbf' : '',
  '\\xc3\\x81' : 'A',
  '\\xc3\\x89' : 'E',
  '\\xc3\\x8d' : 'I',
  '\\xc3\\x91' : 'N',
  '\\xc3\\x93' : 'O',
  '\\xc3\\x9a' : 'U',
  '\\xc3\\x9c' : 'U',
  '\\xc3\\xa1' : 'A',
  '\\xc3\\xa9' : 'E',
  '\\xc3\\xad' : 'I',
  '\\xc3\\xb1' : 'N',
  '\\xc3\\xb3' : 'O',
  '\\xc3\\xba' : 'U',
  '\\xc3\\xbc' : 'U',
  '\'' : '',
  '\\n' : '',
  '&quot;' : ''
}
PATH_TO_TRAIN = './es-en/train/'
PATH_TO_DEV = './es-en/dev/'
PATH_TO_TEST = './es-en/test/'
FILENAME = 'newstest2012'
FILENAME = 'newstest2013'
FILENAME = 'test2'
SP_PUNCTUATION = set(['¿', '¡'])
PRINT_MSGS = not True

def main():
  m1 = M1()

  # Get sp_sentences to translate out of file (no tokenizing yet).
  sp_sentences = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, FILENAME))
  goal_transls = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, FILENAME))

  with open('%s_translated' % FILENAME, 'w') as f:
    for i, sp_sentence in enumerate(sp_sentences):
      if PRINT_MSGS: print '\nSpanish:  %s' % sp_sentence.replace('\n', '')
      translate_sentence(sp_sentence.split(), goal_transls[i], f, m1)


def translate_sentence(sp_words, goal_transl, file_translated, m1):
  en_translation = ''

  for sp_word in sp_words:
    sp_word_stemmed = sp_word  # tokenize_sp_stemmed(sp_word)

    # Typical words.
    if sp_word_stemmed in m1.sp_vocab or sp_word in SP_PUNCTUATION:
      en_translation += '%s ' % m1.top_english_word(sp_word_stemmed)
    # Deals with punctuation, etc. 
    else:
      en_translation += '%s ' % sp_word     # TODO: this part is super bad

  file_translated.write(en_translation + '\n')
  if PRINT_MSGS: print 'English:  %s' % en_translation
  if PRINT_MSGS: print '   Goal:  %s' % goal_transl


def get_lines_of_file(fileName):
  with open(fileName,'r') as f:
    return [line for line in f]


def tokenize_sp_stemmed(sp_sentence):
  ##
    # First we lowercase the line in order to treat capitalized
    # and non-capitalized instances of a single word the same.
  ##
    # Then, repr() forces the output into a string literal UTF-8
    # format, with characters such as '\xc3\x8d' representing
    # special characters not found in typical ASCII.
  line = repr(sp_sentence.lower())
  
  ##
    # Replace all instances of UTF-8 character codes with
    # uppercase letters of the nearest ASCII equivalent. For
    # instance, 'á' becomes '\\xc3\\xa1' becomes 'A'. The
    # purpose of making these special characters uppercase is
    # to differentiate them from the rest of the non-special
    # characters, which are all lowercase.
  for utf8_code, replacement_char in UTF_SPECIAL_CHARS.items():
    line = line.replace(utf8_code, replacement_char)
  
  # Remove any non-whitespace, non-alphabetic characters.
  line = re.sub(r'[^A-z ]', '', line)

  ##
    # Substitute multiple whitespace with single whitespace, then
    # append the cleaned line to the list.
  return ' '.join(line.split())


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  if PRINT_MSGS: print '\n[ Time elapsed: ]   %s' % (str(datetime.now() - startTime))

  
