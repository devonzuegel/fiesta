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
  m = M1()


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
