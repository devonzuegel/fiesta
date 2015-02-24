import sys
import getopt
import os
import math

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

  # Two layers
  def build_hash_table():
    pass

  # Update all values in second layer
  def set_hash_table_vals():
    pass

  # Single-layer
  def build_dict():
    pass

def readFile(fileName):
  """
  * Code for reading a file.  you probably don't want to modify anything here, 
  * unless you don't like the way we segment files.
  """
  contents = []
  f = open(fileName)
  for line in f:
    contents.append(line)
  f.close()
  result = segmentWords('\n'.join(contents)) 
  return result

def segmentWords(s):
  """
   * Splits lines on whitespace for file reading
  """
  return s.split()


def main():
  print 'Hi!'
  # (options, args) = getopt.getopt(sys.argv[1:], 'f')

if __name__ == "__main__":
    main()
    print readFile('./es-en/dev/newstest2012.en')
