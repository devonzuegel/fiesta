# -*- coding: utf-8 -*-

import sys, getopt, os, math, collections, copy, re, codecs, numpy as np
from datetime import datetime
from bisect import bisect_left
from web2py_utils import search
from nltk.util import ngrams
from collections import defaultdict
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
	en_lines = get_lines_of_file(en_file)

	n_lines = len(sp_lines) # also equal to len(en_lines)

	aligned_sentences = [(sp_lines[i], en_lines[i]) for i in range(n_lines)]
	print aligned_sentences

def get_lines_of_file(filepath):
  f = codecs.open(filepath, encoding='utf-8')
  lines = []
  for line in f:
  	line = line.encode('utf-8').lower()
  	for ch in SPECIAL_CHARS:
  		line = line.replace(ch, SPECIAL_CHARS[ch])
  	lines.append(line.split())
  return lines
