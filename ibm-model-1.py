import sys
import getopt
import os
import math


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

class M1:
  # IBM Model1 initialization
  def __init__(self):
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
    self.transl_prob = self.init_transl_probs();


def main():
  print 'Hi!'
  # (options, args) = getopt.getopt(sys.argv[1:], 'f')

if __name__ == "__main__":
    main()
