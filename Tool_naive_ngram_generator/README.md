## Description

it's a rather simple script to generate sentences based on a corpora set and a given starting chunk of a sentence.

e.g. given "I was a"... and the corpora of Jane Austen's 'austen-sense.txt' from nltk's popular set. we could generate a 2nd-or-3rd-order-gram full sentence based on the naive n-gram idea.

for this particular corpus, only n <= 3 is allowed. however, with a larger corpus, we might propogate towards 5-gram or so!

no sanity check, no error handling, just a simple verifying script.

## Usage

run test.py after pip install all the dependencies.
