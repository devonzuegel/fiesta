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

PATH_TO_TRAIN = './es-en/train/'
# PATH_TO_DEV = './es-en/dev/'
FILENAME = 'europarl-v7.es-en'
FILENAME = 'test2'
N_ITERATIONS = 2
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

class M1:

  # IBM Model 1 initialization
  def __init__(self):
    sp_doc = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, FILENAME))
    en_doc = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, FILENAME))
    
    sentence_pairs = self.deconstuct_sentences(sp_doc, en_doc)

    self.build_vocab_indices()

    self.transl_probs = self.train_transl_probs(sentence_pairs)

  ##
  # Build dict for each vocabulary in which keys are words and their
  # values are their respective indices. This will allow lookup of
  # words from row/column in the `transl_probs` & `counts` tables.
  def build_vocab_indices(self):
    self.en_vocab_indices = {}
    self.sp_vocab_indices = {}

    for i in range(0, len(self.en_vocab)):
      word = self.en_vocab[i]
      self.en_vocab_indices[word] = i
    for i in range(0, self.n_sp_words):
      word = self.sp_vocab[i]
      self.sp_vocab_indices[word] = i


  def top_english_word(self, sp_word):
    if sp_word not in self.sp_vocab:
      return sp_word

    sp_row = self.sp_vocab_indices[sp_word]
    i_of_max = np.argmax(self.transl_probs[sp_row])

    return self.en_vocab[i_of_max]  # Top English translation for sp_word


  ##
  # Initialize transl_probs uniformly. It's table from spanish words to
  # english words (list of lists) to probability of that english word being
  # the correct translation. Every translation probability is
  # initialized to (1/# english words) since every word is equally
  # likely to be the correct translation.
  def init_transl_probs(self):
    # Create matrix uniformly filled with `1*uniform_prob`
    uniform_prob = 1.0 / self.n_en_words
    return np.ones((self.n_sp_words, self.n_en_words)) * uniform_prob


  # Create the counts table.
  def init_counts(self):
    return np.zeros((self.n_sp_words, self.n_en_words))

  def train_transl_probs(self, sentence_pairs):

    # Initialize counts and totals to be used in main loop.
    print '\n=== Initializing transl_probs & counts...'
    transl_probs = self.init_transl_probs()
    startTime = datetime.now()
    for x in xrange(0, N_ITERATIONS):
      print '\n=== %d Training translation probabilities...' % (x + 1)
      print 'Time elapsed (BEGIN):   %s' % (str(datetime.now() - startTime))
      counts       = self.init_counts()
      total_s      = [0] * self.n_sp_words


      print 'Time elapsed (BEFORE FIRST LOOP):   %s' % (str(datetime.now() - startTime))
      for pair in sentence_pairs:
        total_e = [0] * self.n_sp_words
        sp_sentence = pair[0].split()
        en_sentence = pair[1].split()

        ##
        # TODO: consider calculating the vocab indices for the entire
        # sentences here so there aren't `2ij` lookups.

        # Spanish words are the rows, English words are the columns
        for en_word in en_sentence:    # Each word in the English sentence
          for sp_word in sp_sentence:  # Each word in the Spanish sentence
            sp_row = self.sp_vocab_indices[sp_word]
            en_col = self.en_vocab_indices[en_word]
            total_e[en_col] += transl_probs[sp_row][en_col]
        
        for en_word in en_sentence:    # Each word in the English sentence
          for sp_word in sp_sentence:  # Each word in the Spanish sentence
            sp_row = self.sp_vocab_indices[sp_word]
            en_col = self.en_vocab_indices[en_word]

            additional_prob = transl_probs[sp_row][en_col] / (1.0*total_e[en_col])
            counts[sp_row][en_col] += additional_prob
            total_s[sp_row] += additional_prob

      print 'Time elapsed (BEFORE SECOND LOOP):   %s' % (str(datetime.now() - startTime))
      for sp_i in range(self.n_sp_words):
        if total_s[sp_i]:
          for en_i in range(self.n_en_words):
            transl_probs[sp_i][en_i] = counts[sp_i][en_i] / (total_s[sp_i] * 1.0)
            # transl_probs[sp_i][en_i] = 0 if (total_s_at_sp_i == 0) else counts[sp_i][en_i] / (total_s_at_sp_i * 1.0)

      print 'Time elapsed (AFTER SECOND LOOP):   %s' % (str(datetime.now() - startTime))
    return transl_probs

  ##
  # Takes in an array of sentences of sp and en words
  # returns tuples in the form of (sp sentence, en sentence)
  def deconstuct_sentences(self, sp_doc, en_doc):
    print '\n=== Deconstructing sentences & building vocabs...'
    ##
    # Iterate through all English & Spanish sentences & add each word
    # to the respective vocabularies.
    en_vocab = set()
    sp_vocab = set()
    for en_sentence in en_doc:
      for en_word in en_sentence.split(' '):
        en_vocab.add(en_word)
    for sp_sentence in sp_doc:
      for sp_word in sp_sentence.split(' '):
        sp_vocab.add(sp_word)
        
    # Build sorted vocab list.
    self.en_vocab = list(sorted(en_vocab))
    self.sp_vocab = list(sorted(sp_vocab))
    self.n_en_words = len(self.en_vocab)
    self.n_sp_words = len(self.sp_vocab)

    # Build list of sentence pair tuples.
    tuples = []
    for i, sp_sentence in enumerate(sp_doc):
      tuples.append((sp_doc[i], en_doc[i]))


    self.n_en_words = len(self.en_vocab)
    self.n_sp_words = len(self.sp_vocab)
    # Return list of sentence pair tuples.
    return tuples


def get_word_indices(sentence, vocab_indices):
  n_words = len(sentence)
  word_indices = [0]*n_words
  for i, word in enumerate(sentence):
    word_indices[i] = vocab_indices[word]
  return word_indices


##
# Code for reading and tokenizing a file.
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


def main():
  m = M1()


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
