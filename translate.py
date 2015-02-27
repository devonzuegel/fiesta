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

def main():
  # m1 = M1()

  sp_sentences = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, 'test0'))

  print sp_sentences

  # sp_sentence = '¿ Qué significa esto ? .'.split()
  # en_translation = ''
  # for sp_word in sp_sentence:
  #   en_translation += ' %s' % m1.top_english_word(sp_word)
  
  # print 'Spanish sentence: ==='
  # print ' '.join(sp_sentence)
  
  # print 'English translation: ==='
  # print en_translation

  # print 'Goal: ==='
  # print 'What does this mean ?'


##
# Code for reading a file.  you probably don't want to modify anything here, 
# unless you don't like the way we segment files.
def get_lines_of_file(fileName):
  lines = []
  with open(fileName,'r') as f: 
    for line in f:
      ##
      # First we lowercase the line in order to treat capitalized
      # and non-capitalized instances of a single word the same.
      ##
      # Then, repr() forces the output into a string literal UTF-8
      # format, with characters such as '\xc3\x8d' representing
      # special characters not found in typical ASCII.
      line = repr(line.lower())
      
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
      
      # Substitute multiple whitespace with single whitespace, then
      # append the cleaned line to the list.
      lines.append(' '.join(line.split()))
  return lines


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
