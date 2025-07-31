import re
import os
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from better_profanity import profanity
import time

phrases = set()

t0_total = time.perf_counter()

#Get distinct names in all of the synsets to process
print("Getting Lemma Names:")
t0 = time.perf_counter()
names = {lemma.name() for synset in wn.all_synsets() for lemma in synset.lemmas()}
t1 = time.perf_counter()
print(f"Gathered names in {t1 - t0:.2f} seconds")

print("Initial filters:")
t0 = time.perf_counter()
for name in names:
    if "_" in name:
        parts = name.split('_')
        #must be 2 words,
        if len(parts) == 2:
            #Must be alphabetic words at least 2 long
            if all(p.isalpha() and len(p) > 1 for p in parts):
                # watch yo profanity, kind of heavy handed profanity chekcer but it works
                if not profanity.contains_profanity(f"{parts[0]} {parts[1]}"):
                    phrases.add(f"{parts[0].lower()} {parts[1].lower()}")
t1 = time.perf_counter()
print(f"Filtered Phrases in {t1 - t0:.2f} seconds")
    
#Now that the list is much smaller, filter out proper nouns
print("Filtering Proper Nouns")
t0 = time.perf_counter()
phrases = {
    p for p in phrases
    if not any(tag in ('NNP', 'NNPS') for _, tag in pos_tag(p.split()))
}
t1 = time.perf_counter()
print(f"Filtered Proper Nouns in {t1-t0:.2f} seconds")

print(f"Number of Phrases: {len(phrases)}")
t1_total = time.perf_counter()
print(f"Finished in {t1_total - t0_total:.2f} seconds")


''' Pre Optimized Code
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
