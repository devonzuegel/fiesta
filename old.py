# -*- coding: utf-8 -*-

import sys
import getopt
import os
import math
import collections
import copy
import re
import pprint

pp = pprint.PrettyPrinter(indent=3)
PATH_TO_DEV = './es-en/dev/'
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
  # IBM Model1 initialization
  def __init__(self):
    #Isolate pairings from documents 
    self.en_vocab = set()
    self.sp_vocab = set()

    sp_doc = get_lines_of_file('%snewstest2012.es' % (PATH_TO_DEV))
    # sp_doc = ["Yo tengo un perro", "Yo tengo"]
    en_doc = get_lines_of_file('%snewstest2012.en' % (PATH_TO_DEV))
    # en_doc = ["I have a dog", "I have"]

    sentence_pairs = self.get_sentence_pairs(sp_doc, en_doc)

    print '... completed sentence_pairs = self.get_sentence_pairs(sp_doc, en_doc) ...'

    ##
    # Initialize transl_probs uniformly (hash from spanish words to hash from english words
    # to probability of that english word beign the correct translation. Every translation
    # probability is initialized to 1/#english words since every word is equally likely to 
    # be the correct translation.)
    self.transl_probs = self.find_probabilities()

    print '... completed self.transl_probs = self.find_probabilities() ...'

    #Initialize counts and totals to be used in main loop. 
   
    # MASSIVE LOOPDELOOP
    # create the counts hash
    temp = dict.fromkeys(self.en_vocab, 0)
    self.counts = {}
    for key in self.sp_vocab:
      self.counts[key] = copy.deepcopy(temp)
    #self.counts = dict.fromkeys(copy.deepcopy(self.sp_vocab), copy.deepcopy(temp))
    
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
    
    #PRint out highest probability pairs: NOT PART OF ALGORITHM
    for spanish_word in self.transl_probs.keys():
      max_prob_engligh_word = "poop"
      max_prob = 0
      for english_word in self.transl_probs[spanish_word].keys():
        if self.transl_probs[spanish_word][english_word] > max_prob:
          max_prob = self.transl_probs[spanish_word][english_word]
          max_prob_engligh_word = english_word
      print spanish_word + ":" + max_prob_engligh_word + ":" + str(max_prob)


  def find_probabilities(self):
    temp = dict.fromkeys(self.en_vocab, 1.0/len(self.en_vocab))
    temp_dict = {}
    for key in self.sp_vocab:
      temp_dict[key] = copy.deepcopy(temp)
    return temp_dict
    #return dict.fromkeys(self.sp_vocab, dict.fromkeys(self.en_vocab, 1.0/len(self.en_vocab)))

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
  # m.find_probabilities()
  

if __name__ == "__main__":
  main()

  
