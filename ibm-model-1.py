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
    # Lowercase everything
    # Build vocab for spanish
    # Build vocab for english

    # n = height
    # self.transl_probs = build_hash_table(1/n)
    # self.counts = build_hash_table(0)

    # total

    self.transl_prob = self.init_transl_probs();


  # Single-layer
  def build_dict(doc_from_single_lang):
    pass


  # [
  #   ("El perro", "The dog")
  #   ("El chico", "The boy")
  # ]
  def sentence_pairs(sp_doc, en_doc):
    pass

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
  dict = {}
  dict['perro'] = collections.defaultdict(lambda: 1)
  dict['tengo'] = collections.defaultdict(lambda: 2)


if __name__ == "__main__":
  main()
  spanish = get_lines_of_file('%snewstest2012.es' % (PATH_TO_DEV))
  english = get_lines_of_file('%snewstest2012.en' % (PATH_TO_DEV))

  print spanish
  print english

  