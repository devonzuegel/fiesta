# -*- coding: utf-8 -*-

import sys
import getopt
import os
import math
import collections
import copy
import re
import pickle
import pprint

pp = pprint.PrettyPrinter(indent=3)

##
# TODO: implement this so that when False, it doesn't fill the
# cache file. Allow this to be a flag!!
CACHE_FILENAME = 'transl_probs.pickle'
DELETE_CACHE = False

path_to_dev = './es-en/dev/'
utf_special_chars = {
  '\\xc2\\xa1' : '',
  '\\xc2\\xbf' : '',
  '\\xc3\\x81' : 'a',
  '\\xc3\\x89' : 'e',
  '\\xc3\\x8d' : 'i',
  '\\xc3\\x91' : 'n',
  '\\xc3\\x93' : 'o',
  '\\xc3\\x9a' : 'u',
  '\\xc3\\x9c' : 'u',
  '\\xc3\\xa1' : 'a',
  '\\xc3\\xa9' : 'e',
  '\\xc3\\xad' : 'i',
  '\\xc3\\xb1' : 'n',
  '\\xc3\\xb3' : 'o',
  '\\xc3\\xba' : 'u',
  '\\xc3\\xbc' : 'u',
  '\'' : '',
  '\\n' : '',
  '&quot;' : ''
}

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

# values for english within spanish word must sum to 1.0
  # {
  #   'yo': {
  #     'i': .3
  #     'have': .4
  #     'dog': .3
  #   }
  #   'tengo': {
  #     'i': .3
  #     'have': .4
  #     'dog': .3
  #   }
  #   'perro': {
  #     'i': .3
  #     'have': .4
  #     'dog': .3
  #   }
  # }
class m1:
  # ibm model1 initialization
  def __init__(self):
    #isolate pairings from documents 
    self.en_vocab = set()
    self.sp_vocab = set()

    # sp_doc = get_lines_of_file('%seuroparl-v7.es-en.es' % (path_to_dev))
    sp_doc = ["yo tengo un perro", "yo tengo", "perro es mio", "yo soy devon", "tengo perro"]
    # en_doc = get_lines_of_file('%seuroparl-v7.es-en.en' % (path_to_dev))
    en_doc = ["i have a dog",      "i have",   "dog is mine",  "i am devon",   "have dog"]

    sentence_pairs = self.get_sentence_pairs(sp_doc, en_doc)

    ##
    # initialize transl_probs uniformly (hash from spanish words to hash from english words
    # to probability of that english word beign the correct translation. every translation
    # probability is initialized to 1/#english words since every word is equally likely to 
    # be the correct translation.)   
    self.transl_probs = self.init_transl_probs()

    # Initialize counts and totals to be used in main loop. 
    self.init_counts_table()
    

    print '------------ CALCULATING TRALSATION PROBABILITIES .... ------------'
    if os.path.exists(CACHE_FILENAME):
      print 'Cache file exists!'
      # Load values from file.
      with open(CACHE_FILENAME, "rb") as f:     self.transl_probs = pickle.load(f) 
    else:
      print 'Cache does not yet exist. Finding translation probabilities now...'
      # Find translation probabilities.
      self.execute_algorithm(sentence_pairs)
      # Save into file.
      with open(CACHE_FILENAME, 'wb') as f:     pickle.dump(self.transl_probs, f)     
    
    print '------------ DONE CALCULATING TRALSATION PROBABILITIES ------------'

    # Print out highest probability translation for each word.
    self.highest_prob_pairs()


  def init_transl_probs(self):
    temp = dict.fromkeys(self.en_vocab, 1.0/len(self.en_vocab))
    temp_dict = {}
    for key in self.sp_vocab:
      temp_dict[key] = copy.deepcopy(temp)
    return temp_dict


  def init_counts_table(self):
    self.counts = {}
    temp = dict.fromkeys(self.en_vocab, 0)
    for key in self.sp_vocab:
      self.counts[key] = copy.deepcopy(temp)


  def execute_algorithm(self, sentence_pairs, n_iterations=1):
    # TODO: making n_interations > 1 gets us probabilities greater than 1...! :(
    for x in xrange(0, n_iterations):
      self.total_s = dict.fromkeys(self.sp_vocab, 0)
      for pair in sentence_pairs:
        self.total_e = dict.fromkeys(self.en_vocab, 0)
        sp_sentence = pair[0]
        en_sentence = pair[1]
        for english_word in en_sentence.split():
          for spanish_word in sp_sentence.split():
            self.total_e[english_word] += self.transl_probs[spanish_word][english_word]
        for english_word in en_sentence.split():
          for spanish_word in sp_sentence.split():
            self.counts[spanish_word][english_word] += (self.transl_probs[spanish_word][english_word] *1.0/ self.total_e[english_word])
            self.total_s[spanish_word] += (self.transl_probs[spanish_word][english_word] / self.total_e[english_word])

      for spanish_word in self.sp_vocab:
        for english_word in self.en_vocab:
          self.transl_probs[spanish_word][english_word] = (self.counts[spanish_word][english_word] / self.total_s[spanish_word])


  # Print out highest probability pairs.
  def highest_prob_pairs(self):
    for spanish_word in self.transl_probs.keys():
      max_prob_engligh_word = "poop"
      max_prob = 0
      for english_word in self.transl_probs[spanish_word].keys():
        if self.transl_probs[spanish_word][english_word] > max_prob:
          max_prob = self.transl_probs[spanish_word][english_word]
          max_prob_engligh_word = english_word
      print spanish_word + ":" + max_prob_engligh_word + "  " + str(max_prob)

  #takes in an array of sentences of sp and en words
  #returns tuples in the form of (sp sentence, en sentence)
  def get_sentence_pairs(self, sp_doc, en_doc):
    tuples = []
    for en_sentence in en_doc:
      for en_word in en_sentence.split(' '):
        self.en_vocab.add(en_word)
    for sp_sentence in sp_doc:
      for sp_word in sp_sentence.split(' '):
        self.sp_vocab.add(sp_word)
      
    for i, sp_sentence in enumerate(sp_doc):
      tuples.append((sp_doc[i], en_doc[i]))
    return tuples


##
# code for reading a file.  you probably don't want to modify anything here, 
# unless you don't like the way we segment files.
def get_lines_of_file(filename):
  lines = []
  with open(filename,'r') as f: 
    for line in f:
      ##
      # First we lowercase the line in order to treat capitalized
      # and non-capitalized instances of a single word the same.
      ##
      # Then, repr() forces the output into a string literal utf-8
      # format, with characters such as '\xc3\x8d' representing
      # special characters not found in typical ascii.
      line = repr(line.lower())
      
      ##
      # Replace all instances of utf-8 character codes with
      # uppercase letters of the nearest ascii equivalent. for
      # instance, 'á' becomes '\\xc3\\xa1' becomes 'a'. the
      # purpose of making these special characters uppercase is
      # to differentiate them from the rest of the non-special
      # characters, which are all lowercase.
      for utf8_code, replacement_char in utf_special_chars.items():
        line = line.replace(utf8_code, replacement_char)
      
      # Remove any non-whitespace, non-alphabetic characters.
      line = re.sub(r'[^a-z ]', '', line)
      
      # Substitute multiple whitespace with single whitespace, then
      # append the cleaned line to the list.
      lines.append(' '.join(line.split()))
  return lines


def offer_to_delete_cache():
  DELETE_CACHE = False

  if os.path.exists(CACHE_FILENAME):
    r = raw_input('Delete the existing cache? (y/n): ').lower()
    DELETE_CACHE = (r == 'y') or (r == 'yes')

    if DELETE_CACHE:
      print '------------ DELETING CACHE .... ------------'
      os.remove(CACHE_FILENAME)


if __name__ == "__main__":
  offer_to_delete_cache()
  m = m1()  
