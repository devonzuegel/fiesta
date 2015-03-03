# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, codecs, re, nltk
from datetime import datetime
from bisect import bisect_left
from nltk.tag import pos_tag
from IBMModel1_2 import M1


SPECIAL_CHARS = {
  '\xc3\x81' : 'A',
  '\xc3\x89' : 'E',
  '\xc3\x8d' : 'I',
  '\xc3\x91' : 'N',
  '\xc3\x93' : 'O',
  '\xc3\x9a' : 'U',
  '\xc3\x9c' : 'U',
  '\xc3\xa1' : 'A',
  '\xc3\xa9' : 'E',
  '\xc3\xad' : 'I',
  '\xc3\xb1' : 'N',
  '\xc3\xb3' : 'O',
  '\xc3\xba' : 'U',
  '\xc3\xbc' : 'U',
  '\xc2\xbf' : '', # upside down question mark
  '\xc2\xa1' : '', # upside down exclamation mark
  '\n' : ''
}


def translate(sp_sentences, m1):
  translns_file = open('%s_translations' % FILENAME, 'w')
  en_translns = []
  print '\n== English translations:'
  for sp_sentence in sp_sentences:
    en_transln = ''

    for sp_word in sp_sentence:
      en_word = m1.max_prob_alignment(sp_word)
      if en_word is not None:  
        en_transln += '%s ' % (en_word)

    print en_transln

    en_translns.append(en_transln)
    translns_file.write(en_transln + '\n')
  translns_file.close()


def get_lines_of_file(filepath):
  f = codecs.open(filepath, encoding='utf-8')
  lines = []
  for line in f:
    line = line.encode('utf-8').lower()
    for ch in SPECIAL_CHARS:
      line = line.replace(ch, SPECIAL_CHARS[ch])
    lines.append(line.split())
  return lines


if __name__ == "__main__":
  startTime = datetime.now()
  if len(sys.argv) < 2:
    print '\nRequires the path to and name of file (without .en/.es extension) to translate:'
    print 'Usage:  $ python translate.py ./PATH/TO/FILE/ FILENAME'
    print 'Aborting...'
  else:
    filepath_to_train = './es-en/train/' + raw_input('\n== Filename to train on? ')
    PATH, FILENAME = sys.argv[1], sys.argv[2]

    # Get sp_sentences to translate out of file (no tokenizing)
    sp_sentences = get_lines_of_file('%s%s.es' % (PATH, FILENAME))
    # Get goal_sentences to compare translations to out of file (no tokenizing)
    goal_translns = get_lines_of_file('%s%s.en' % (PATH, FILENAME))

    n_iterations = int(raw_input('\n== # of iterations? '))
    # Initialize IBM Model 1 class.
    m1 = M1(filepath_to_train, n_iterations)
    
    translate(sp_sentences, m1)
    os.system('python bleu_score.py %s%s.en %s_translations' % (PATH, FILENAME, FILENAME))

  print '\n[ Time elapsed: ]   %s\n' % (str(datetime.now() - startTime))
