# Fiesta: A Spanish to English Translator
[Devon Zuegel](mailto:devonz@cs.stanford.edu), [Zoe Robert](mailto:zrobert7@stanford.edu), and [John Luttig](mailto:jluttig@stanford.edu) &nbsp; // &nbsp; February 2015

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents ##
- [Overview](#overview)
    - [BLEU Scores](#bleu-scores)
    - [Running Fiesta](#running-fiesta)
    - [Structure of this repo](#structure-of-this-repo)
- [Spanish-specific challenges](#spanish-specific-challenges)
- [Improvement upon baseline strategy](#improvement-upon-baseline-strategy)
- [Other modifications](#other-modifications)
- [Error Analysis](#error-analysis)
- [IBM Model 1](#ibm-model-1)
    - [Pseudocode](#pseudocode)
- [Comparative Analysis with Google Translate](#comparative-analysis-with-google-translate)
    - [Spanish Sentences](#spanish-sentences)
    - [Our Output](#our-output)
    - [Google Translate Output](#google-translate-output)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview
Fiesta is based on the IBM Model 1 Expectation Maximation algorithm and implements several Spanish-specific strategies for improving word ordering within the English translations that result from the IBM M1 algorithm.

#### BLEU Scores ####
Our most recent BLEU scores are as follows:
```
BLEU-1 score: 49.539586
BLEU-2 score: 10.110798
```


#### Running Fiesta ####

To generate the translation probabilities, translate a given `.es` file, and evaluate the resulting translations, run the following command:
```shell
$ python translate.py PATH_TO_FILE FILENAME
```
The first arg is the path to the file you wish to translate, and the second is the name of the `.es` file *without its extension*. For example, to run the program over the test set:
```shell
$ python translate.py ./es-en/test/ newstest2013
```
The program will then ask you for the name of the file on which you'd like to train the probabilities table. For example, to train over the `europarl` test set:
```shell
$ == Filename to train on? europarl-v7.es-en
```
Then, tell it the number of iterations you would like the algorithm to perform (in the following case, `20`):
```shell
$ == number of iterations? 20
```
The program may take up to 20 minutes to run on the full train+test sets. Then, it will output the BLUE-1 and BLUE-2 scores.


#### Structure of this repo ####
This repo contains bitext data for Spanish-English (es-en). Training data are selected from the Europarl-v7 corpus, and dev/test data are from its corresponding development set.

All data have been tokenized such that each line is a sentence, and all tokens are separated by spaces. Special characters such as apostrophes are escaped in a form similar to HTML special characters (&apos;). Lines with the same line number from the beginning of the files of corresponding languages are source/target sentence pairs (i.e. source sentence and its translation).

## Spanish-specific challenges ##
There are several key differences between English and Spanish that played into our translation algorithm design.

1. One difficulty of Spanish in particular is the way in which it tends to combine verbs and their subjects. For example, Spanish has many verbs such as “cocinamos”, meaning “we cook”. This is challenging because Spanish communicates in 1 word what often takes 2 or more words in English.

2. Spanish verbs are more varied in their form for a given verb. For example, the English phrase “I cook” can be easily translated as two separate words. In Spanish, however, “cocino” is a different word from “cocinas”, even though the refer to the same action.

3. Spanish often orders its adjectives and nouns differently in a sentence. For example, “casa verde” means “green house”, even though “casa” translates to “house” and “verde” translates to “green”.

4. Question phrases in spanish do not necessarily include the subject. For example, the Spanish sentence “¿Quien es?” refers to a subject implicitly (“he”) but does not say it, even though the English equivalent is “Who is he?” (“Who is?” wouldn’t make sense). There are exceptions to this rule that make it tricky: in Spanish, you CAN say “¿Quien es él?” – including the subject explicitly if you would like.

5. In Spanish, one can use the word “no” to denote a variety of things, which in English ends up being expanded in some way, into “do not”, or “did not”, or “does not”.

6. There are certain idioms that have no simple translation. For example, “Tengo hambre” means “I am hungry”, even though “tengo” does not translate to “am”. Thus, these phrases must either be hard-coded or accounted for outside of single-word translations, using a more sophisticated bigram model that recognizes the probability of the orders of certain words (in the above example, it would recognize that “I have hungry” is an extremely unlikely sequence).

## Improvement upon baseline strategy ##
1. Our first strategy to improve the baseline IBM mode 1 system was to improve its speed. We accomplished this using numpy instead of the nested lists and hashes that we had previously used. Once our speed was reasonable, we could perform tests quickly enough to implement complex algorithms. We started with Bigrams, since it was something we were familiar with from previous assignments. We also kept tabs on Piazza and Office Hours to sift through the optimization ideas to find the more successful algorithms.

2. We implemented part-of-speech tagging and reordering once back in English. Thus we would map each word to its part of speech, and perform post-processing operations on the sentence for special cases. Specifically, any time we saw an adjective following a noun, we flipped the two so that the adjective would come first, as it always does in English but doesn’t always do in Spanish.

3. We uppercased only the accented characters to differentiate between words in Spanish that are identical except for accented characters. This allows a finer granularilty of translation. For example, we provided the following distinction:
```
union » union
uniòn » uniOn
```

## Other modifications ##
We tried a few things that didn’t seem to improve the translator:

1. We built a bigram English-language model and then tried to extract the most likely permutation of the translated English “bag of words” with that model. Running through each permutation of every sentence took a long time, so we were forced to take it out of the translator. We tried to think of better ways to go about extracting candidates from the permutations so we wouldn’t have to run through so many, but after brainstorming and implementing several ideas it didn’t seem to improve the model and remained prohibitively slow.

2. Instead of simply returning the word with the highest translation probability from the IBM Model 1 matrix, out of the top `n` words we returned the one with the lowest Levenshtein edit distance. However, this slightly reduced our score, so we left it commented out.

3. We place a greater weight on the `NULL` word. This opens up the possibility for two Spanish words translating to a single English word.

## Error Analysis ##
We had many errors throughout our coding process, so we’ve distilled our favorites here:

1. One error that we had is the commonality of repeated rare words in sentence. For example, “Premio Nobel de la Paz” translates to “nobel nobel of the peace”. This is a nice effort, but the issue comes when “nobel” is repeated twice in the translation. This happens because the word “nobel” is rare, and is only seen in a few sentence throughout the corpus. Therefore, both “premio” and “nobel” translate to “nobel”. We found a solution around this error: once a rare word has been translated once in a sentence, it will not be translated again. We initially tried to solve the issue by disallowing repeat words entirely, but this did more harm than good when it came to words often seen multiple times in a sentence, like “the” and “in”. We then chose to allow repeat words in a sentence as long as the word is not in the top 10% most popular words by its unigram sequence.

2. Another error that our algorithm encountered is the use of the Spanish phrase “of the” surrounding proper nouns. For example, “Premio Nobel de la Paz” is actually “Nobel Peace Prize”, leaving out the “of the” entirely. This errors stems from the difference in possessives between English and Spanish - in Spanish, it is very common to use “de” or “de la” to denote possession, whereas in English, possession can be written as “John’s car” or “the car of John”. We did not explicitly solve this problem, but we have a potential solution. Determine where proper nouns are throughout the sentence (this can be as simple as finding capitalized words not at the beginning) and remove any “de” or “de la” around them. It is possible that this modification would cause more harm than good, but it has a good chance of success because proper nouns combined with “de” are relatively uncommon. If one were to implement this modification, it’d be good to experiment with removing “de la” entirely or replacing it with some sort of apostraphe to reverse the order. We implemented a rudimentary version of this, as follows, after translating each English line:
```
line = re.sub(r’.* (.*?) of the (.*?) .*’, r”\g<2>’s \g<1>”, line)
```

### IBM Model 1
IBM Model 1 is an **expectation-maximization statistical alignment algorithm**. Given known pairings of Spanish and English sentences, it generates a matrix of probabilities whose rows correspond to the Spanish vocabulary and columns correspond to the English vocabulary. The value at any given cell in the matrix represents the probability that those two words have co-occurred within translations of each other. This table is then used to estimate a model for future translations.

In short, IBM Model 1 looks for the most likely English word for a Spanish word (e.g. “dog”) based off our knowledge of co-occurrences within sentences. As such, if there are no translations of a given Spanish word `s` that contain a given English word `e`, the value of the cell at the corresponding row and column will be `0`.

The algorithm requires 3 components:

- a language model to compute `P(E)` (the prior)
- a translation model to compute `P(S|E)` (the probability that a Spanish word `s` translates to an English word `e`)
- a decoder that produces that most probable
Further information on p. 876 of the textbook.

#### Pseudocode ####

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

## Comparative Analysis with Google Translate

1. The first sentence the big difference between our output and Google translate output is lack of a good translation of the verb exigirlo. Neither seems like a good tranlslaiton, but Google does a slightly better job beucase they translate the verb.  
2/ Our translation didn’t properly swap adjective and noun “republican representatives” while Google did, additionally our ver translation is not as good as Google’s. 

2. The error in this sentence stems from the fact that our translator doesn’t deal with spanish verbs properly. In this instance, it seems like Google tranlsation was more effective because the verb translation included the subject “yo”, while our tranlation did not. 

3. Once again, the Google tranlsation is preferred because our translation uses more awkward language. “five adolescent of between ten and 15 years” is much less natural sounding than “five boys aged between ten and 15 years.” 

4. This sentence Google’s translation is preferred because it generally makes more sense. Specifically, “immediately” is a better translation than “of immediate”.

#### Spanish Sentences ####

1. El Estado de Indiana, fue, el primero, en exigirlo.

2. Este fen\xf3meno se ha extendido tras las elecciones de noviembre de 2010, que vieron el aumento de 675 nuevos representantes republicanos en 26 estados.

3. Lo recuerdo perfectamente. 

4. el Periódico entrevistó a cinco muchachos de entre diez y 15 años , usuarios frecuentes de la red .

5. De inmediato no hubo un pronunciamiento de Warner ni de TNT sobre cómo manejará la serie la pérdida de Hagman .

#### Our Output ####

1. the state of indiana was the first in. 

2. this phenomenon be has widespread following are elections of november of 2010 , that saw the increase of 675 new representatives republicans in 26 states . 

3. what remember perfectly .

4. enquire to five adolescent of between ten and 15 years , users frequent of the network . 

5. of immediate not tribunal a usual of aol nor of tnt about how the series the loss of hagman .

#### Google Translate Output ####

1. The State of Indiana was the first on demand it.

2. This fen \ xf3meno has spread after the elections of November 2010, which saw an increase of 675 new Republican representatives in 26 states.

3. I remember it perfectly.

4. elPeriódico interviewed five boys aged between ten and 15 years, frequent users of the network.

5. Immediately there was a pronouncement of Warner or TNT on how to handle the series loss Hagman.