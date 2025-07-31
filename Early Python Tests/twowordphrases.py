import re
import os
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from better_profanity import profanity



phrases = set()
valid_word = re.compile(r"^[a-zA-Z]{2,}$") #only alphabetic words more than 2 long

#All synsets in Wordnet
for synset in wn.all_synsets():
    for lemma in synset.lemmas():
        #Each synset has associated words or multiword terms
        name = lemma.name()
        parts = name.split('_')

        #must be 2 words
        if len(parts) != 2:
            continue

        #Skip non-alphabetic words (i.e. anything with punctuation, numbers, and anything less than one letter)
        if not all(valid_word.match(part) for part in parts):
            continue

        #Skip if proper noun, 'NNP' Proper noun singular, 'NNPS' proper noun plural
        tags = pos_tag(parts)
        if any(tag in ('NNP', 'NNPS') for _, tag in tags):
            continue
        
        phrase = ' '.join(parts).lower()
        #watch yo profanity,
        #kind of heavy handed profanity checker, but it works
        if not profanity.contains_profanity(phrase):
            phrases.add(phrase)
        

'''
output_file = "two_word_phrases.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for p in sorted(phrases):
        f.write(p + "\n")
'''