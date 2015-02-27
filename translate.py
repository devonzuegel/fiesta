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

from IBMModel1 import M1

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
FILENAME = 'test2'
SPANISH_PUNCTUATION = set(['¿', '¡'])

def main():
  m1 = M1()

  # Get sp_sentences to translate out of file (no tokenizing)
  sp_sentences = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, FILENAME))
  goal_transln = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, FILENAME))

  for i, sp_sentence in enumerate(sp_sentences):
    print '\n'
    print 'Spanish:  %s' % sp_sentence.replace('\n', '')

    sp_words = sp_sentence.split()
    en_translation = ''

    for sp_word in sp_words:
      sp_word_stemmed = tokenize_sp_stemmed(sp_word)

      # Deals with punctuation, etc. 
      if sp_word_stemmed not in m1.sp_vocab and sp_word not in SPANISH_PUNCTUATION:
        en_translation += '%s ' % sp_word     # TODO: this part is super bad
      # Typical words
      else:
        en_translation += '%s ' % m1.top_english_word(sp_word_stemmed)
        # print '%s  :  %s' % (sp_word, sp_word_stemmed)

    # For each sp_word in sp_sentence_tokenized
      # Get the best translation for that specific word
      # Add it sentence (later put in bag for order, but for now keep same order)
    # Print the resulting English sentence

  # for sp_sentence in sp_sentences:
  #   sp_words = sp_sentence.split()
  #   en_translation = ''

  #   print '\n================================\n'
  #   for sp_word in sp_words:
  #     sp_word_tokenized =
  #     en_translation += '%s ' % m1.top_english_word(sp_word)
    
  #   print '\n=== Spanish sentence: ==='
  #   print ' '.join(sp_words)
    
    print 'English:  %s' % en_translation
    print '   Goal:  %s' % goal_transln[i]

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
  print '\n[ Time elapsed: ]   %s' % (str(datetime.now() - startTime))

  
