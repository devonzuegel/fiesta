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


PATH_TO_TRAIN = './es-en/train/'
PATH_TO_DEV = './es-en/dev/'
# FILENAME = 'europarl-v7.es-en'
FILENAME = 'test2'
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


def binary_search(to_search, val, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi or len(to_search)              # hi defaults to len(a)   
    pos = bisect_left(to_search, val, lo, hi)   # find insertion position
    return pos if pos != hi and to_search[pos] == val else -1 # don't walk off the end

##
  # initialize transl_prob(e|f) uniformly
  # do until convergence
  #   set count(e|f) to 0 for all e,f
  #   set total(f) to 0 for all f
  #   for all sentence pairs (e_s,f_s)
  #     set total_s(e) = 0 for all e
  #     for all words e in e_s
  #       for all words f in f_s
  #         total_s(e) += transl_prob(e|f)
  #     for all words e in e_s
  #       for all words f in f_s
  #         count(e|f) += transl_prob(e|f) / total_s(e)
  #         total(f)   += transl_prob(e|f) / total_s(e)
  #   for all f
  #     for all e
  #       transl_prob(e|f) = count(e|f) / total(f)

# Values for english within spanish word must sum to 1.0
  # {
  #   'Yo': {
  #     'I': .3
  #     'have': .4
  #     'dog': .3
  #   }
  #   'tengo': {
  #     'I': .3
  #     'have': .4
  #     'dog': .3
  #   }
  #   'perro': {
  #     'I': .3
  #     'have': .4
  #     'dog': .3
  #   }
  # }
class M1:

  # IBM Model 1 initialization
  def __init__(self):
    sp_doc = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, FILENAME))
    en_doc = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, FILENAME))
    
    sentence_pairs = self.deconstuct_sentences(sp_doc, en_doc)
  
    transl_probs = self.train_transl_probs(sentence_pairs)

    print_best_translations(transl_probs, self.sp_vocab, self.en_vocab)

  ##
    # Initialize transl_probs uniformly. It's table from spanish words to
    # english words (list of lists) to probability of that english word being
    # the correct translation. Every translation probability is
    # initialized to (1/# english words) since every word is equally
    # likely to be the correct translation.
  def init_transl_probs(self):
    ##
    # Initialize the "rows" (corresponding to a Spanish word) for the
    # `transl_probs` table.
    transl_probs = [None] * len(self.sp_vocab)

    # Get the size of the english vocab.
    num_english_words = len(self.en_vocab)
    # Compute a starting prob, initially uniform to all entries.
    starting_prob = 1.0/num_english_words

    ##
    # Initalize a single row. Each column should begin with the same
    # starting probability, which will later be updated through the
    # algorithm.
    row = [starting_prob] * num_english_words

    ##
    # For each row (corresponding to a Spanish word), make a DEEP COPY
    # of that row so that they can be updated as individuals (as
    # opposed to all pointing to the same list).
    for i in range(0, len(transl_probs)):
      transl_probs[i] = row[0:]

    return transl_probs


  # Create the counts table.
  def init_counts(self):
    ##
    # Initialize the "rows" (corresponding to a Spanish word) for the
    # `counts` table.
    counts = [None] * len(self.sp_vocab)

    # Get the size of the english vocab.
    num_english_words = len(self.en_vocab)

    ##
    # Initalize a single row. Each column should begin with the same
    # starting probability, which will later be updated through the
    # algorithm.
    row = [0] * num_english_words

    ##
    # For each row (corresponding to a Spanish word), make a DEEP COPY
    # of that row so that they can be updated as individuals (as
    # opposed to all pointing to the same list).
    for i in range(0, len(counts)):
      counts[i] = row[0:]

    return counts


  def train_transl_probs(self, sentence_pairs):

    # Initialize counts and totals to be used in main loop. 
    print '\n=== Initializing transl_probs & counts...'
    transl_probs = self.init_transl_probs()
    counts       = self.init_counts()
    total_s      = [0] * len(self.sp_vocab)

    print '\n=== Training translation probabilities...'
    for pair in sentence_pairs:
      total_e = [0] * len(self.sp_vocab)
      sp_sentence = pair[0].split()
      en_sentence = pair[1].split()

      ##
      # Find index of each word in the sentence (both Spanish & English)
      # in the `self.e*_vocab` sorted list.
      sp_word_indices = get_word_indices(sp_sentence, self.sp_vocab)
      en_word_indices = get_word_indices(en_sentence, self.en_vocab)

      for e in range(len(en_sentence)):    # Each index `e` in English sentence
        for s in range(len(sp_sentence)):  # Each index `s` in Spanish sentence
          sp_row = sp_word_indices[s]  # Spanish words » rows of all tables
          en_col = en_word_indices[e]  # English words » cols of all tables

          total_e[en_col] += transl_probs[sp_row][en_col]
      
      for e in range(len(en_sentence)):    # Each index `e` in English sentence
        for s in range(len(sp_sentence)):  # Each index `s` in Spanish sentence
          sp_row = sp_word_indices[s]  # Spanish words » rows of all tables
          en_col = en_word_indices[e]  # English words » cols of all tables

          counts[sp_row][en_col] += transl_probs[sp_row][en_col] / (1.0*total_e[en_col])
          total_s[sp_row] += transl_probs[sp_row][en_col] / (1.0*total_e[en_col])

    for sp_i in range(len(self.sp_vocab)):
      for en_i in range(len(self.en_vocab)):
        if total_s[sp_i] == 0:
          transl_probs[sp_i][en_i] = 0
        else:
          transl_probs[sp_i][en_i] = counts[sp_i][en_i] / (total_s[sp_i] * 1.0)

    return transl_probs

  ##
  # Takes in an array of sentences of sp and en words
  # returns tuples in the form of (sp sentence, en sentence)
  def deconstuct_sentences(self, sp_doc, en_doc):
    print '\n=== Deconstructing sentences & building vocabs...'
    self.en_vocab_indices = {}
    self.sp_vocab_indices = {}

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

    ##
    # Build dict for each vocabulary in which keys are words and their
    # values are their respective indices. This will allow lookup of
    # words from row/column in the `transl_probs` & `counts` tables.
    for i in range(0, len(self.en_vocab)):
      word = self.en_vocab[i]
      self.en_vocab_indices[word] = i
    for i in range(0, len(self.sp_vocab)):
      word = self.sp_vocab[i]
      self.sp_vocab_indices[word] = i
  
    # Build list of sentence pair tuples.
    tuples = []
    for i, sp_sentence in enumerate(sp_doc):
      tuples.append((sp_doc[i], en_doc[i]))

    # Return list of sentence pair tuples.
    return tuples

def print_best_translations(transl_probs, sp_vocab, en_vocab):
  for sp_row in range(len(transl_probs)):
    row = transl_probs[sp_row]
    max_prob = max(row)
    i_of_max = row.index(max_prob)
    # print '%s : %s    %f' % (sp_vocab[sp_row], en_vocab[i_of_max], max_prob)


def get_word_indices(sentence, vocab):
  n_words = len(sentence)
  word_indices = [0]*n_words
  for i, word in enumerate(sentence):
    word_indices[i] = binary_search(vocab, word)
  return word_indices


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


def main():
  m = M1()


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
