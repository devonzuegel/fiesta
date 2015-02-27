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

PATH_TO_TRAIN = './es-en/train/'
# PATH_TO_DEV = './es-en/dev/'
FILENAME = 'europarl-v7.es-en'
FILENAME = 'test2'



def main():
  m1 = M1()
  sp_sentence = 'Ahora bien , se ha demostrado que no es así .'.split()
  en_translation = ''
  for sp_word in sp_sentence:
    en_translation += ' %s' % m1.top_english_word(sp_word)
  print ' '.join(sp_sentence)
  print en_translation
  print 'Goal: "However, at this stage these are just proposals."'
if __name__ == "__main__":
  startTime = datetime.now()
  main()
  print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
