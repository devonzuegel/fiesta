# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, re, nltk
from datetime import datetime
from bisect import bisect_left
from nltk.tag import pos_tag
from IBMModel1_2 import M1


if __name__ == "__main__":
  startTime = datetime.now()
  if len(sys.argv) < 2:
    print '\nRequires the path to and name of file (without .en/.es extension) to translate:'
    print 'Usage:  $ python translate.py ./PATH/TO/FILE/ FILENAME'
    print 'Aborting...'
  else:
    filepath_to_train = './es-en/train/test2'
    filepath_to_translate = '%s%s' % (sys.argv[1], sys.argv[2])

    m1 = M1(filepath_to_train, 20)
    
  #   # Print bleu_score
  #   bleu_cmd = 'python bleu_score.py %s%s.en %s_translations' % (path, filename, filename)
  #   os.system(bleu_cmd)
    
  print '\n[ Time elapsed: ]   %s\n' % (str(datetime.now() - startTime))

  
