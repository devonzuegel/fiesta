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
class M1(object):
	def __init__(self, filepath, n_iterations):
		sentence_pairs = get_sentence_pairs(filepath)

		##
		# vocabs['sp'] = alphabetical Spanish vocab list
		# vocabs['en'] = alphabetical English vocab list
		self.vocabs = extract_vocabs(sentence_pairs)

		self.en_unigram_counts = get_unigram_counts([p[1] for p in sentence_pairs])

		##
		# self.vocab_indices['sp'] = maps words to their indices in vocabs['sp']
		# self.vocab_indices['en'] = maps words to their indices in vocabs['en']
		self.vocab_indices = extract_vocab_indices(self.vocabs)

		# Trains alignment probabilities for each possible Sp-En pairing.
		self.probabilities = self.train(sentence_pairs, self.vocabs, n_iterations)
		
		print_matrix(self.vocabs, self.probabilities)
		# print '\n== Probabilities:'
		# print self.probabilities
		# print self.vocabs['sp']
		# print self.vocabs['en']


	def train(self, sentence_pairs, vocabs, n_iterations):
		init_prob = 1 / (len(vocabs['en']) * 1.0)
		probabilities = np.ones( (len(vocabs['sp']), len(vocabs['en'])) ) * init_prob
		print_matrix(vocabs, probabilities)
		for i in range(0, n_iterations):
			print '\n=== Iteration %d/%d' % (i+1, n_iterations)
	
			fractnl_counts = np.zeros((len(vocabs['sp']), len(vocabs['en'])))
			total = [0] * len(vocabs['sp'])

			for sp_tokens, en_tokens in sentence_pairs:
				# sp_tokens = sp_tokens# + [ None ]  # Prepend `None` to Spanish sentence list
				# en_tokens = en_tokens  # Prepend `None` to English sentence list
				total_sp = [0] * len(vocabs['en'])
				# Normalize P(a,S|E) values to yield P(a|E,F) values.
				total_sp = self.normalize(total_sp, en_tokens, sp_tokens, probabilities)

				for en_word in en_tokens:
					en_i = self.vocab_indices['en'][en_word]
					for sp_word in sp_tokens:
						sp_i = self.vocab_indices['sp'][sp_word]
						additnl_prob = probabilities[sp_i][en_i] / (total_sp[en_i] * 1.0)
						fractnl_counts[sp_i][en_i] += additnl_prob
						total[sp_i] += additnl_prob

			total_reshaped = np.asarray(total).reshape(len(total), 1)
			probabilities = fractnl_counts / (total_reshaped * 1.0)

		return probabilities


	def max_prob_alignment(self, sp_word):
		# If the word isn't in our Spanish vocabulary (and thus doesn't have
		# a row in the translation probabilities matrix), simply return itself.
		if sp_word not in self.vocabs['sp']: 	return sp_word

		sp_i = self.vocab_indices['sp'][sp_word]
		en_candidates = copy.deepcopy(self.probabilities[sp_i])

		##
		# Scale prob for each word by its frequency.
		for en_word in en_candidates:
			en_candidates[en_word] = en_candidates[en_word] * self.en_unigram_counts[en_word]

		# Get index of max probability of the English word candidates.
		i_of_max = np.argmax(en_candidates)

		# Return the highest probability English candidate.
		return self.vocabs['en'][i_of_max]


	def normalize(self, total_sp, en_tokens, sp_tokens, probabilities):
		for en_word in en_tokens:
			en_i = self.vocab_indices['en'][en_word]
			for sp_word in sp_tokens:
				sp_i = self.vocab_indices['sp'][sp_word]
				total_sp[en_i] += probabilities[sp_i][en_i]
		return total_sp


def estimate_probs(probabilities, vocabs, total_sp):
	for i,s in enumerate(vocabs['sp']):
		for j,e in enumerate(vocabs['en']):
			# print str(probabilities[i][j]) + ' ' + str(total_sp[i])
			probabilities[i][j] = 0 if (total_sp[i] == 0) else probabilities[i][j] / (total_sp[i] * 1.0)
	return probabilities



def extract_vocabs(sentence_pairs):
	sp_vocab, en_vocab = set([]), set([])
	for sp_line, en_line in sentence_pairs:
		sp_vocab |= set(sp_line)
		en_vocab |= set(en_line)

	# sp_vocab.add(None)  # Add null token to the Spanish vocab
	return {  'sp': sorted(sp_vocab),  'en': sorted(en_vocab)  }


def get_unigram_counts(sentences):
	counts = defaultdict(lambda: 0)
	for sentence in sentences:
		for word in sentence:
			counts[word] += 1
	return counts


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


def print_matrix(vocabs, probabilities):
	column = '{:<%d}' % 10
	lines = []
	
	# Build header row (English words, underlined).
	headers = column.format('')
	for e, en_word in enumerate(reversed(vocabs['en'])):
		headers += column.format(en_word)
	lines += [headers]
	lines += [column.format('') + '-------------------------------------']
	
	# Build each row (sp_word:  0.##  0.##  0.##  ...).
	for s, sp_word in enumerate(reversed(vocabs['sp'])):
		row = ''
		for prob in probabilities[s]:
			row += column.format(round(prob, 4))
		lines += [column.format(sp_word) + row]

	# Print the table.
	for l in lines:			print l

def get_lines_of_file(filepath):
  f = codecs.open(filepath, encoding='utf-8')
  lines = []
  for line in f:
  	line = line.encode('utf-8').lower()
  	for ch in SPECIAL_CHARS:
  		line = line.replace(ch, SPECIAL_CHARS[ch])
  	lines.append(line.split())
  return lines
