from nltk.corpus import wordnet as wn
import os

phrases = set()

# Go through every synset in WordNet
for syn in wn.all_synsets():
    # Each synset has lemmas (words or multiword terms)
    for lemma in syn.lemmas():
        name = lemma.name()  
        parts = name.split('_')
        # Only keep phrases that are exactly two words
        if len(parts) == 2:
            phrase = ' '.join(parts).lower()
            phrases.add(phrase)

output_file = "wordnet_two_word_phrases.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for p in sorted(phrases):
        f.write(p + "\n")