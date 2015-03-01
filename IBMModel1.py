# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, re, numpy as np
from datetime import datetime
from bisect import bisect_left
from web2py_utils import search
from nltk.util import ngrams
from collections import defaultdict

leve = search.Levenshtein()

PATH_TO_TRAIN = './es-en/train/'
# PATH_TO_DEV = './es-en/dev/'
FILENAME = 'europarl-v7.es-en'
FILENAME = 'test2'
N_ITERATIONS = 20
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
}
USE_CACHE = True
CACHE_FILE = 'transl_probs_cache'
PRINT_MSGS = not True

class M1:

  # IBM Model 1 initialization
  def __init__(self):
    sp_doc = get_lines_of_file('%s%s.es' % (PATH_TO_TRAIN, FILENAME))
    en_doc = get_lines_of_file('%s%s.en' % (PATH_TO_TRAIN, FILENAME))
    
    sentence_pairs = self.deconstuct_sentences(sp_doc, en_doc)

    self.build_vocab_indices()

    user_input = raw_input('Use cached transl_probs? (y/n): ')
    if user_input.lower() == 'y' and os.path.exists(CACHE_FILE):
      print 'Loading transl_probs from cache...'
      with open(CACHE_FILE, 'rb') as f:
        self.transl_probs = np.loadtxt(CACHE_FILE)
    else:
      print 'Building transl_probs...'
      self.transl_probs = self.train_transl_probs(sentence_pairs)
      with open(CACHE_FILE, 'w') as f:
        np.savetxt(CACHE_FILE, self.transl_probs)


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
    # Deal with unknown words.
    if sp_word not in self.sp_vocab:  return sp_word

    sp_row = self.sp_vocab_indices[sp_word]

    adjusted_probs = copy.deepcopy(self.transl_probs[sp_row]) #self.transl_probs
    for i in range(len(adjusted_probs)):
      adjusted_probs[i] /= self.get_unigram_probability(self.en_vocab[i])
    i_of_max = np.argmax(adjusted_probs)

    ## Makes the score worse, so take it out for now. :(
    # return self.word_with_lowest_edit_dist(sp_word, adjusted_probs)

    return self.en_vocab[i_of_max]  # Top English translation for sp_word

  
  def word_with_lowest_edit_dist(self, sp_word, adjusted_probs):
    indices_of_best = []
    for i in range(2):
      i_of_best = np.argmax(adjusted_probs)
      indices_of_best.append(i_of_best)
      adjusted_probs[i_of_best] = 0
    best_list = [self.en_vocab[i] for i in indices_of_best]
    
    return leve.suggestion(sp_word, best_list, number_of_matches=1)[0][1]

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
    if PRINT_MSGS: print '\n=== Initializing transl_probs & counts...'
    transl_probs = self.init_transl_probs()
    startTime = datetime.now()
    for x in xrange(0, N_ITERATIONS):
      if PRINT_MSGS: print '\n=== %d Training translation probabilities...' % (x + 1)
      if PRINT_MSGS: print 'Time elapsed (BEGIN):   %s' % (str(datetime.now() - startTime))
      counts = self.init_counts()
      total_s = [0] * self.n_sp_words

      if PRINT_MSGS: print 'Time elapsed (BEFORE FIRST LOOP):   %s' % (str(datetime.now() - startTime))
      for pair in sentence_pairs:
        total_e = [0] * self.n_sp_words
        sp_sentence, en_sentence = pair[0].split(), pair[1].split()

        ##
        # Calculating the vocab indices for each word in both sentences
        # sentences here so there aren't `2ij` lookups within the loops.
        sp_word_indices = get_word_indices(sp_sentence, self.sp_vocab_indices)
        en_word_indices = get_word_indices(en_sentence, self.en_vocab_indices)

        # Spanish words are the rows, English words are the columns
        for e in range(len(en_sentence)):    # Each word in the English sentence
          en_col = en_word_indices[e]
          for s in range(len(sp_sentence)):  # Each word in the Spanish sentence
            sp_row = sp_word_indices[s]
            total_e[en_col] += transl_probs[sp_row][en_col]
        
        for e in range(len(en_sentence)):    # Each word in the English sentence
          en_col = en_word_indices[e]
          for s in range(len(sp_sentence)):  # Each word in the Spanish sentence
            sp_row = sp_word_indices[s]
            additional_prob = transl_probs[sp_row][en_col] / (1.0*total_e[en_col])
            counts[sp_row][en_col] += additional_prob
            total_s[sp_row] += additional_prob

      if PRINT_MSGS: print 'Time elapsed (BEFORE SECOND LOOP):   %s' % (str(datetime.now() - startTime))
      
      total_s_reshaped = np.asarray(total_s).reshape(len(total_s), 1)
      transl_probs = counts / (total_s_reshaped * 1.0)
      if PRINT_MSGS: print 'Time elapsed (AFTER SECOND LOOP):   %s' % (str(datetime.now() - startTime))
    return transl_probs


  def get_unigram_probability(self, sp_word):
    return self.en_unigram_counts[sp_word] * (1.0) / self.total_n_en_words

  ##_en # Takes in an array of sentences of sp and en words
  # returns tuples in the form of (sp sentence, en sentence)
  def deconstuct_sentences(self, sp_doc, en_doc):
    if PRINT_MSGS: print '\n=== Deconstructing sentences & building vocabs...'
    ##
    # Iterate through all English & Spanish sentences & add each word
    # to the respective vocabularies.
    en_vocab, sp_vocab = set(), set()
    self.en_unigram_counts = collections.defaultdict(lambda:0) 
    self.total_n_en_words = 0
    self.en_bigram_counts = defaultdict(lambda: 0, {})

    for en_sentence in en_doc:
      en_tokens = en_sentence.split(' ')
      for i in range(len(en_tokens)):
        curr_en_word = en_tokens[i]
        
        if i+1 < len(en_tokens):
          bigram = '%s %s' % (en_tokens[i], en_tokens[i+1])
          self.en_bigram_counts[bigram] += 1


        self.en_unigram_counts[curr_en_word] += 1
        en_vocab.add(curr_en_word)
        self.total_n_en_words += 1
    for sp_sentence in sp_doc:
      sp_tokens = sp_sentence.split(' ')
      for sp_word in sp_tokens:   sp_vocab.add(sp_word)
        
    # Build sorted vocab list.
    self.en_vocab, self.sp_vocab = list(sorted(en_vocab)), list(sorted(sp_vocab))

    # Save size of the Spanish & English vocabs in self attribute.
    self.n_en_words, self.n_sp_words = len(self.en_vocab), len(self.sp_vocab)

    # Build list of sentence pair tuples.
    return [(sp_doc[i], en_doc[i]) for i, sp_sentence in enumerate(sp_doc)]



def get_word_indices(sentence, vocab_indices):
  return [vocab_indices[word] for i, word in enumerate(sentence)]



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
      line = re.sub(r'[^A-z&; ]', '', line)
      
      # Substitute multiple whitespace with single whitespace, then
      # append the cleaned line to the list.
      lines.append(' '.join(line.split()))
  return lines


def main():
  m = M1()


if __name__ == "__main__":
  startTime = datetime.now()
  main()
  if PRINT_MSGS: print 'Time elapsed:   %s' % (str(datetime.now() - startTime))

  
