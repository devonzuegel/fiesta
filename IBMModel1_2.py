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

		##
		# vocabs['sp'] = alphabetical Spanish vocab list
		# vocabs['en'] = alphabetical English vocab list
		vocabs = extract_vocabs(sentence_pairs)

		##
		# vocab_indices['sp'] = maps words to their indices in vocabs['sp']
		# vocab_indices['en'] = maps words to their indices in vocabs['en']
		vocab_indices = extract_vocab_indices(vocabs)

		# Trains alignment probabilities for each possible Sp-En pairing.
		self.probabilities = self.train(sentence_pairs, vocabs, vocab_indices, n_iterations)


	def train(self, sentence_pairs, vocabs, vocab_indices, n_iterations):
		init_prob = 1.0/len(vocabs['en'])
		probabilities = defaultdict(lambda: defaultdict(lambda: init_prob))
		total_en = {  en_word:0 for en_word in vocabs['en']  }

		for i in range(0, n_iterations):
			counts = defaultdict(lambda: defaultdict(lambda: 0.0))
			total_sp = defaultdict(lambda: 0.0)

			for sp_tokens, en_tokens in sentence_pairs:
				sp_tokens = [None] + sp_tokens  # Prepend `None` to Spanish sentence list

				total_en = normalize(total_en, en_tokens, sp_tokens, probabilities)

def normalize(total_en, en_tokens, sp_tokens, probabilities):
	for en_word in en_tokens:
		total_en[en_word] = 0.0
		for sp_word in sp_tokens:
			total_en[en_word] += probabilities[en_word][sp_word]
	return total_en

def extract_vocabs(sentence_pairs):
	sp_vocab, en_vocab = set([]), set([])
	for sp_line, en_line in sentence_pairs:
		sp_vocab |= set(sp_line)
		en_vocab |= set(en_line)

	sp_vocab.add(None)  # Add null token to the Spanish vocab
	return {  'sp': sorted(sp_vocab),  'en': sorted(en_vocab)  }


def extract_vocab_indices(vocabs):
	sp_vocab_indicies = {  sp_word:i for i,sp_word in enumerate(vocabs['sp'])  }
	en_vocab_indicies = {  en_word:i for i,en_word in enumerate(vocabs['en'])  }
	return {  'sp': sp_vocab_indicies,  'en': en_vocab_indicies  }


def get_sentence_pairs(filepath):
	sp_file = '%s.es' % (filepath)
	en_file = '%s.en' % (filepath)

	sp_lines = get_lines_of_file(sp_file)
	en_lines = get_lines_of_file(en_file)

	n_lines = len(sp_lines) # also equal to len(en_lines)

	return [(sp_lines[i], en_lines[i]) for i in range(n_lines)]


def get_lines_of_file(filepath):
  f = codecs.open(filepath, encoding='utf-8')
  lines = []
  for line in f:
  	line = line.encode('utf-8').lower()
  	for ch in SPECIAL_CHARS:
  		line = line.replace(ch, SPECIAL_CHARS[ch])
  	lines.append(line.split())
  return lines
