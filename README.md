## Notes
### IBM Model 1

Further information on p. 880 of the textbook.


### Expectation-Maximization Statistical Machine Translation (EM Statistical MT)
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


## Our strategy to improve the baseline IBM Model 1 system
*Your strategy to improve the baseline IBM model 1 system*


## Error analysis on the test set
*Your error analysis on the test set, including specific reference to what your code does and ideas for how further work might fix your remaining errors.*


## Comparative Analysis with Google Translate
*A comparative analysis commenting on your system's performance compared to Google Translate's. Show where the systems agree, what your system does better than Google Translate, and what Google Translate does better than your system.*


## Structure of this repo
This repo contains bitext data for Spanish-English (es-en). Training data are selected from the Europarl-v7 corpus, and dev/test data are from its corresponding development set.

All data have been tokenized such that each line is a sentence, and all tokens are separated by spaces. Special characters such as apostrophes are escaped in a form similar to HTML special characters (&apos;). Lines with the same line number from the beginning of the files of corresponding languages are source/target sentence pairs (i.e. source sentence and its translation).