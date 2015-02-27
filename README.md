# Fiesta: README

[Zoe Robert](mailto:zrobert7@stanford.edu), [Devon Zuegel](mailto:devonz@cs.stanford.edu), and [John Luttig](mailto:jluttig@stanford.edu)


## IBM Model 1
- A **statistical alignment** algorithm
- We're looking for the most likely English word for a Spanish word (e.g. "dog") based off our knowledge of co-occurrences within sentences.


The general IBM Model 1 generative story for how we generate a Spanish sentence from an English sentence `E = e1,e2,...,ei` of length `i`:
1. Choose a length `j` for the Spanish sentence, henceforth `F = f1, f2,..., fj`.
2. Now choose an alignment `A = a_1,a_2, ... ,a_j` between the English and Spanish
sentences.
3. Now for each position `j` in the Spanish sentence, choose a Spanish word `fj` by translating the English word that is aligned to it.

Further information on p. 880 of the textbook.

```
# Values for english within spanish word must sum to 1.0
# TODO: might be the other way aroundd!!!
{
  'Yo': {
    'I': .3
    'have': .4
    'dog': .3
  }
  'tengo': {
    'I': .3
    'have': .4
    'dog': .3
  }
  'perro': {
    'I': .3
    'have': .4
    'dog': .3
  }
}
```

---

## To Do

### Programming

- [x] implement IBM Model 1 on `train/` folder (Zoe, Tuesday/Wednesday)
- [x] fix ascii-unicode-latin1 encoding issues (Devon, Tuesday night)
- [x] implement caching with pickle in `transl_probs.pickle` (Devon, Wednesday night)
- [x] multiple iterations
- [x] self.sp_word_indices dictionary instead of binary search
- [x] optimize algorithm ( @luttigdev )
- [x] lowercase? DOESN'T MATTER
- [x] add english language model (single-word probabilities) (Zoe, Thursday)
- [x] **implement evaluation/run-through for `dev/` folder through Bleu ASAP**
- [ ] bigrams ( @luttigdev, Zoe)
- [ ] decide new priorities once we get Bleu working
- [ ] Viterbi + nltk (parts of speech tagging » reordering Sp-Eng verbs for exmaple)
  - NOTE: can't tag single English words because not enough context
- [ ] conjugations in Spanish indicate subject ("Tengo" == "Yo tengo") ... deal with this!

### Questions
- [ ] logs
- [x] COGNATES (not a good idea)

## Misc
- [ ] shouldn't remove commas from translation...
- [ ] Shouldn't remove &quot; and similar thingies
- [ ] Check out random \x word (devon)


### Report To Dos
- [ ] A comment on the language F that you chose. You should make a brief statement of particular challenges in translating your choice of F language to English (relative to other possible choices for F), and key insights about the language that you made use of in your strategies to improve your baseline MT system.
- [] Your strategy to improve the baseline IBM model 1 system
- [ ] Your error analysis on the test set, including specific reference to what your code does and ideas for how further work might fix your remaining errors.
- [ ] The output of Google Translate.
- [ ] A comparative analysis commenting on your system's performance compared to Google Translate's. Show where the systems agree, what your system does better than Google Translate, and what Google Translate does better than your system.



### Report
##Language Choice: Spanish
We chose Spanish because of our relative backgrounds in Spanish compared to the alternative languages. One difficulty of Spanish in particular is the way in which it tends to combine verbs and their subjects. For example, Spanish has many verbs such as "cocinamos", meaning "we cook". This is challenging because Spanish communicates in 1 word what often takes 2 or more words.

Our first strategy to improve the baseline IBM mode 1 system was to improve its speed. We accomplished this using numpy instead of the nested lists and hashes that we had previously used. Once our speed was reasonable, we could perform tests quickly enough to implement complex algorithms. We started with Bigrams, since it was something we were familiar with from previous assignments. We also kept tabs on Piazza and Office Hours to sift through the optimization ideas to find the more successful algorithms.

---

## Pseudocode

```python
initialize transl_prob(e|f) uniformly
do until convergence
  set count(e|f) to 0 for all e,f
  set total_s(f) to 0 for all f
  for all sentence pairs (en_sentence, sp_sentence)
    set total_e(e) = 0 for all e
    for all words e in en_sentence
      for all words f in sp_sentence
        total_e(e) += transl_prob(e|f)
    for all words e in en_sentence
      for all words f in sp_sentence
        count(e|f) += transl_prob(e|f) / total_e(e)
        total_s(f)   += transl_prob(e|f) / total_e(e)
  for all f
    for all e
      transl_prob(e|f) = count(e|f) / total_s(f)
```


# Useful resources & links
- [Pseudocode](http://www.ims.uni-stuttgart.de/institut/mitarbeiter/fraser/readinggroup/model1.html)
- [An implementation](https://github.com/kylebgorman/model1/blob/master/m1.py)
- [p. 880 of the textbook](https://web.stanford.edu/class/cs124/restricted/ed2mt.pdf)


## Expectation-Maximization Statistical Machine Translation (EM Statistical MT)
Requires 3 components:
- a language model to compute `P(E)` (the prior)
- a translation model to compute `P(S|E)` ()
- a decoder that produces that most probable

Further information on p. 876 of the textbook.


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

## Our strategy to improve the baseline IBM Model 1 system
*Your strategy to improve the baseline IBM model 1 system*
- IBM Model 1 makes some major simplifying assumptions. One of the most egregious is the assumption that all align- ments are equally likely.

## Error analysis on the test set
*Your error analysis on the test set, including specific reference to what your code does and ideas for how further work might fix your remaining errors.*


## Comparative Analysis with Google Translate
*A comparative analysis commenting on your system's performance compared to Google Translate's. Show where the systems agree, what your system does better than Google Translate, and what Google Translate does better than your system.*


## Structure of this repo
This repo contains bitext data for Spanish-English (es-en). Training data are selected from the Europarl-v7 corpus, and dev/test data are from its corresponding development set.

All data have been tokenized such that each line is a sentence, and all tokens are separated by spaces. Special characters such as apostrophes are escaped in a form similar to HTML special characters (&apos;). Lines with the same line number from the beginning of the files of corresponding languages are source/target sentence pairs (i.e. source sentence and its translation).
