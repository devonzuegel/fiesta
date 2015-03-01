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
import nltk
from nltk.tag import pos_tag
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
  '\\xf3' : 'O',
  '\'' : '',
  '\\n' : '',
}
PATH_TO_TRAIN = './es-en/train/'
SP_PUNCTN = set(['¿', '¡'])
PRINT_MSGS = not True

def main(filename):
  m1 = M1()

  # Get sp_sentences to translate out of file (no tokenizing)
  sp_sentences = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, filename))
  goal_translns = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, filename))

  # Opens file into which will dump our translations line-by-line.
  translns_file = open('%s_translations' % filename, 'w')

  
  ##
  # Asks user if they only want to use basic IBM Model 1 or also use noun-adj
  # flipping + bigram ordering to refine their results.
  user_response = raw_input('\nTranslate with just IBM Model 1? (y/n) ').lower()
  just_ibm_m1 = user_response == 'y'

  print 'Translating sentences...'
  for i, sp_sentence in enumerate(sp_sentences):
    sp_sentence = nltk.word_tokenize(sp_sentence.decode("utf-8"))
    translate_sentence(sp_sentence, m1, translns_file, goal_translns[i], just_ibm_m1)

  translns_file.close()

def get_lines_of_file(filename):
  with open(filename,'r') as f:
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

  ##
    # Substitute multiple whitespace with single whitespace, then
    # append the cleaned line to the list.
  return ' '.join(line.split())

def translate_sentence(sp_sentence, m1, translns_file, goal_transln, just_ibm_m1):
  if PRINT_MSGS: print '\nSpanish:  %s' % sp_sentence.replace('\n', '')

  en_translation = ''

  for sp_word in sp_sentence:
    sp_word = tokenize_sp_stemmed(sp_word.encode('utf-8'))

    if sp_word not in m1.sp_vocab and sp_word not in SP_PUNCTN:
      en_translation += '%s ' % sp_word     # TODO: this part is super bad
    else:
      en_translation += '%s ' % m1.top_english_word(sp_word)

  if not just_ibm_m1:
    en_translation = order_sentence(en_translation.encode('utf-8'))
  
  translns_file.write(en_translation + '\n')
  if PRINT_MSGS: print 'English:  %s' % en_translation
  if PRINT_MSGS: print '   Goal:  %s' % goal_transln

def order_sentence(en_translation):
  return flip_nouns_adjs(en_translation)

# For each adjective, if the prev word is a noun, flip the two.
def flip_nouns_adjs(en_transln):
  # Tokenizes `en_transln` then tags each token
  tagged = pos_tag(nltk.word_tokenize(en_transln.decode("utf-8")))

  for i in range(1, len(tagged)):
    prev_tupl, curr_tupl = tagged[i-1], tagged[i]
    prev_POS,  curr_POS  = prev_tupl[1], curr_tupl[1]

    prev_is_noun = prev_POS=='NN' or prev_POS=='NNS' or prev_POS=='NNP' or prev_POS=='NNPS'
    curr_is_adjv = curr_POS == 'JJ'
    # If you see an adjective after a noun, flip them.
    if curr_is_adjv and prev_is_noun:
      tagged[i-1] = curr_tupl
      tagged[i] = prev_tupl

  return ' '.join([t[0].encode('utf-8') for t in tagged])


if __name__ == "__main__":
  startTime = datetime.now()
  if len(sys.argv) < 2:
    print 'Requires name of file to translate. Aborting...'
  else:
    filename = sys.argv[1]
    main(filename)
    
    # Print bleu_score
    bleu_cmd = 'python bleu_score.py es-en/train/%s.en %s_translations' % (filename, filename)
    os.system(bleu_cmd)
    
    print '\n[ Time elapsed: ]   %s' % (str(datetime.now() - startTime))

  
