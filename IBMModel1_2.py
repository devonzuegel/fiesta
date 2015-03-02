# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, re, codecs, numpy as np
from datetime import datetime
from bisect import bisect_left
from web2py_utils import search
from nltk.util import ngrams
from collections import defaultdict

##
# This class implements the IBM Model 1 algorithm of Expectation Maximization.
class Model1(object):
	def __init__(self, filepath, n_iterations):
		sentence_pairs = get_sentence_pairs(filepath)
		# self.probabilities = self.train()
		

def get_sentence_pairs(filepath):
	sp_file = '%s.es' % (filepath)
	en_file = '%s.en' % (filepath)

	sp_lines = get_lines_of_file(sp_file)
	print sp_lines
	en_lines = get_lines_of_file(en_file)

	n_lines = len(sp_lines) # also equal to len(en_lines)

	aligned_sentences = [(sp_lines[i], en_lines[i]) for i in range(n_lines)]
	# print aligned_sentences

def get_lines_of_file(filepath):
  f = codecs.open(filepath, encoding='utf-8')
  for line in f:
  	print line.encode('utf-8')
  return [line.encode('utf-8') for line in f]
