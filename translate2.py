# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, re, nltk
from datetime import datetime
from bisect import bisect_left
from nltk.tag import pos_tag
from IBMModel1 import M1
from IBMModel1_2 import Model1


if __name__ == "__main__":
  startTime = datetime.now()
  model1 = Model1('./es-en/train/test2', 5)
  # if len(sys.argv) < 2:
  #   print 'Requires name of file to translate. Aborting...'
  # else:
  #   path = sys.argv[1]
  #   filename = sys.argv[2]
  #   main(path, filename)
    
  #   # Print bleu_score
  #   bleu_cmd = 'python bleu_score.py %s%s.en %s_translations' % (path, filename, filename)
  #   os.system(bleu_cmd)
    
  #   print '\n[ Time elapsed: ]   %s' % (str(datetime.now() - startTime))

  
