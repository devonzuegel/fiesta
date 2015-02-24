import sys
import getopt
import os
import math
import collections
import re

PATH_TO_DEV = './es-en/dev/'

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
    self.en_vocab = []
    self.sp_vocab = []

    sp_doc = get_lines_of_file('%snewstest2012.es' % (PATH_TO_DEV))
    en_doc = get_lines_of_file('%snewstest2012.en' % (PATH_TO_DEV))

    sentence_pairs = self.get_sentence_pairs(sp_doc, en_doc)

    ##
    # Initialize transl_probs uniformly (hash from spanish words to hash from english words
    # to probability of that english word beign the correct translation. Every translation
    # probability is initialized to 1/#english words since every word is equally likely to 
    # be the correct translation.)
    self.transl_probs = self.find_probabilities()

    #Initialize counts and totals to be used in main loop. 
    self.counts = dict.fromkeys(self.sp_vocab, dict.fromkeys(self.en_vocab, 0))
    self.total = dict.fromkeys(self.sp_vocab, 0)
    self.total_s = dict.fromkeys(self.en_vocab, 0)


  def find_probabilities(self):
    return dict.fromkeys(self.sp_vocab, dict.fromkeys(self.en_vocab, 1.0/len(self.en_vocab)))


  #takes in an array of sentences of sp and en words
  #returns tuples in the form of (sp sentence, en sentence)
  def get_sentence_pairs(self, sp_doc, en_doc):
    tuples = []
    for en_sentence in en_doc:
      for en_word in en_sentence.split(' '):
        self.en_vocab.append(en_word)
    for sp_sentence in sp_doc:
      for sp_word in sp_sentence.split(' '):
        self.sp_vocab.append(sp_word)
      
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
      clean_line = ' '.join(re.sub(r'[^A-z ]', '', line.lower()).split())
      lines.append(clean_line)
  return lines


def main():
  m = M1()
  # m.find_probabilities()
  

if __name__ == "__main__":
  main()

  
