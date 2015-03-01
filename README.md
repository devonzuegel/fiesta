# Fiesta: A Spanish to English Translator

[Devon Zuegel](mailto:devonz@cs.stanford.edu), [Zoe Robert](mailto:zrobert7@stanford.edu), and [John Luttig](mailto:jluttig@stanford.edu) &nbsp; // &nbsp; February 2015

## Overview
Fiesta is based on the IBM Model 1 Expectation Maximation algorithm and implements several Spanish-specific strategies for improving word ordering within the English translations that result from the IBM M1 algorithm.

### Running Fiesta
To generate the translation probabilities, translate a given `.es` file, and evaluate the resulting translations, run the following command:
```
$ python translate.py PATH_TO_FILE FILENAME
```

The first arg is the path to the file you wish to translate, and the second is the name of the `.es` file *without its extension*. For example, to run the program over the test set:
```
$ python translate.py ./es-en/test/ newstest2013
```

### IBM Model 1
IBM Model 1 is an **expectation-maximization statistical alignment algorithm**. Given known pairings of Spanish and English sentences, it generates a matrix of probabilities whose rows correspond to the Spanish vocabulary and columns correspond to the English vocabulary. The value at any given cell in the matrix represents the probability that those two words have co-occurred within translations of each other. This table is then used to estimate a model for future translations.

In short, IBM Model 1 looks for the most likely English word for a Spanish word (e.g. "dog") based off our knowledge of co-occurrences within sentences. As such, if there are no translations of a given Spanish word `s` that contain a given English word `e`, the value of the cell at the corresponding row and column will be `0`.

The algorithm requires 3 components:

- a language model to compute `P(E)` (the prior)
- a translation model to compute `P(S|E)` (the probability that a Spanish word `s` translates to an English word `e`)
- a decoder that produces that most probable

Further information on p. 876 of the textbook.

#### Pseudocode
```python
initialize transl_prob(e|s) uniformly
do until convergence
  set count(e|s) to 0 for all e,s
  set total_s(s) to 0 for all s
  for all sentence pairs (en_sentence, sp_sentence)
    set total_e(e) = 0 for all e
    for all words e in en_sentence
      for all words s in sp_sentence
        total_e(e) += transl_prob(e|s)
    for all words e in en_sentence
      for all words s in sp_sentence
        count(e|s) += transl_prob(e|s) / total_e(e)
        total_s(s) += transl_prob(e|s) / total_e(e)
  for all s
    for all e
      transl_prob(e|s) = count(e|s) / total_s(s)
```

### Further strategies

- part-of-speech tagging and reordering once back in English; specifically, any time we saw an adjective following a noun, we flipped the two so that the adjective would come first, as it always does in English but doesn't always do in Spanish.

Things we tried that didn't seem to improve the translator:

- built a bigram English-language model and then tried to extract the most likely permutation of the translated English "bag of words" with that model. Running through each permutation of every sentence took forever, so we were forced to take it out of the translator. We tried to think of better ways to go about extracting candidates from the permutations so we wouldn't have to run through so many, but after brainstorming and implementing several ideas it didn't seem to improve the model and remained immensely slow.

- Instead of simply returning the word with the highest translation probability from the IBM Model 1 matrix, out of the top `n` words we returned the one with the lowest Levenshtein edit distance. However, this too hurt our score, so we left it commented out.

- greater weight on the `NULL` word.

## Spanish-specific challenges
*A comment on the language F that you chose. You should make a brief statement of particular challenges in translating your choice of F language to English (relative to other possible choices for F), and key insights about the language that you made use of in your strategies to improve your baseline MT system.*

- gendered pronouns and articles
- "The bottle floated out." vs. "La botella salio flotando."
- "I am hungry." vs. "Tengo hambre."
- "I'm cold." vs. "Me hace frio
- removed spanish accented characters
  - uppercased only the accented characters to differentiate between words in Spanish that are identical except for accented characters
```
union » union
uniòn » uniOn
```
- conjugations in Spanish indicate subject ("Tengo" == "Yo tengo")
- word ordering is very lax in Spanish, difficult to extract ordering ... bigrams theoretically would help a lot.

## Our strategy to improve the baseline IBM Model 1 system
*Your strategy to improve the baseline IBM model 1 system*
IBM Model 1 makes some major simplifying assumptions. One of the worst is the assumption that all alignments are equally likely.

## Error analysis on the test set
*Your error analysis on the test set, including specific reference to what your code does and ideas for how further work might fix your remaining errors.*


## Comparative Analysis with Google Translate
*A comparative analysis commenting on your system's performance compared to Google Translate's. Show where the systems agree, what your system does better than Google Translate, and what Google Translate does better than your system.*


## Structure of this repo
This repo contains bitext data for Spanish-English (es-en). Training data are selected from the Europarl-v7 corpus, and dev/test data are from its corresponding development set.

All data have been tokenized such that each line is a sentence, and all tokens are separated by spaces. Special characters such as apostrophes are escaped in a form similar to HTML special characters (&apos;). Lines with the same line number from the beginning of the files of corresponding languages are source/target sentence pairs (i.e. source sentence and its translation).
