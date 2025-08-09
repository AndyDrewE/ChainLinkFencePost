import re
import os
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from better_profanity import profanity
import time

phrases = set(['bake off', 'bake sale', 'bake well', 'bath mat', 'bath mat', 'bath robe', 
		   'bath room', 'bath salts', 'bath sponge', 'bath towel', 'bed room', 'black belt', 
		   'black board', 'black smith', 'black stone', 'board cover', 'board game', 'board meeting', 
		   'board room', 'board walk', 'book shelf', 'bottle cap', 'bottle neck', 'bottle opener', 
		   'boy scout', 'building manager', 'camp fire', 'camp ground', 'camp site', 'cap gun', 
		   'cap stone', 'chain link', 'chain mail', 'chain reaction', 'chain saw', 'code switch', 
		   'done for', 'easy bake', 'easy living', 'fence gate', 'fence line', 'fence post', 
		   'game board', 'game card', 'game master', 'game night', 'game on', 'game over', 
		   'game room', 'game token', 'garden gate', 'garden path', 'garden room', 'garden wall', 
		   'general manager', 'general store', 'girl scout', 'green house', 'guest bed', 'guest room', 
		   'hot topic', 'in side', 'kitchen sink', 'last word', 'leader board', 'light beam', 
		   'light house', 'light switch', 'link fence', 'lock box', 'lock pick', 'lock smith', 
		   'lock step', 'mail box', 'mail carrier', 'mail room', 'mail route', 'mail slot', 
		   'master bath', 'master chief', 'mix bowl', 'mix tape', 'mountain pass', 'mountain trail', 
		   'ocean breeze', 'off side', 'office building', 'office chair', 'office door', 'office light', 
		   'office space', 'over easy', 'post card', 'post code', 'post mark', 'post office', 
		   'room mate', 'scout badge', 'scout camp', 'scout leader', 'scout troop', 'show girl', 
		   'sink hole', 'slide show', 'sponge bath', 'stone bridge', 'stone floor', 'stone path', 
		   'stone step', 'stone wall', 'store room', 'switch blade', 'switch board', 'switch gear', 
		   'tape recorder', 'trail guide', 'trail head', 'trail map', 'trail mix', 'trail sign', 
		   'water bottle', 'water front', 'water line', 'water mark', 'water pipe', 'water slide', 
		   'water softener', 'water well', 'well done', 'word game', 'word smith', 'apple pie',
		   'pie crust', 'granny smith', 'apple tart', 'wood panel', 'panel show', "stone quarry", 
		   "trail runner", "office plant", "board member", "mail truck", "post route", 
		   "garden shed", "room key", "switch lock", "water shed", "game show", "stone arch", "board fence", 
		   "trail junction", "water tank", "light post", "stop light", "cross road", "road runner", "runner up",
		   "up side", "upside down", "down side", "out side", "side on", "tape worm", "tape dispenser", 
		   "worm hole", "hole punch", "hole cutter", "hole saw", "hole cover", "hole filler", "hole trap", 
		   "hole plug", "hole opener", "hole drill", "hole finder", "show stopper", "show stop", "stop light", 
		   "stop sign", "down vote", "down payment", "down time", "down stairs", "down town", "down hill", 
		   "down load", "down pour", "down draft", "down swing", "up time", "up town", "up hill", "up stairs",
		    "side door", "side walk", "side table", "side mirror", "side window", "side panel", "side track", 
		    "side street", "side wall", "side view", "smith shop", "shop keep", "apple orchard", "pizza crust",
		    "bath bomb", "word play", "code word",  "trail blaze", "camp stove", "game piece", 
		    "lock jaw", "board state", "mail bag"])

# ---------------- new: config for "sciency" ----------------
# WordNet lexnames that skew scientific/technical. Tweak as needed.
SCIENCY_LEXNAMES = {
    # nouns
    "noun.phenomenon", "noun.process", "noun.quantity", "noun.substance",
    "noun.body", "noun.animal", "noun.plant", "noun.shape", "noun.cognition",
    "noun.relation", "noun.motive", "noun.attribute", "noun.state",
    # verbs often technical; we don't use verbs in patterns, but keep for phrase synsets
    "verb.cognition", "verb.change", "verb.perception",
}
# Heuristic substrings for obviously scientific terms of art
SCIENCY_SUBSTRINGS = (
    "ology", "physics", "chemistry", "bio", "neuro", "geo", "thermo",
    "quantum", "algebra", "calculus", "topology", "matrix", "enzyme",
)

def is_sciency_word(w: str) -> bool:
    # Check WordNet lexname buckets for any synset of the *word*
    for s in wn.synsets(w):
        if s.lexname() in SCIENCY_LEXNAMES:
            return True
    # Quick substring heuristic (lowercase)
    wl = w.lower()
    return any(sub in wl for sub in SCIENCY_SUBSTRINGS)

def is_sciency_phrase(w1: str, w2: str) -> bool:
    # If either token is sciency, or the *phrase* itself (as water_bottle) lands in sciency lexnames
    if is_sciency_word(w1) or is_sciency_word(w2):
        return True
    us = f"{w1}_{w2}"
    for s in wn.synsets(us):
        if s.lexname() in SCIENCY_LEXNAMES:
            return True
    return False
# -----------------------------------------------------------

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
        #must be 2 words
        if len(parts) == 2:
            #Must be alphabetic words at least 2 long
            if all(p.isalpha() and len(p) > 1 for p in parts):
                #Filter obvious proper nouns
                if not any(p[0].isupper() for p in parts):
                    # watch yo profanity
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

# ---------------- new: keep only ADJ+NOUN or NOUN+NOUN ----------------
print("Applying POS pattern filter (ADJ+NOUN, NOUN+NOUN)")
t0 = time.perf_counter()
ALLOWED = {("JJ","NN"), ("JJ","NNS"), ("NN","NN"), ("NN","NNS"), ("NNS","NN"), ("NNS","NNS")}
phrases = {
    p for p in phrases
    if tuple(tag for _, tag in pos_tag(p.split())) in ALLOWED
}
t1 = time.perf_counter()
print(f"Applied POS pattern filter in {t1 - t0:.2f} seconds")

# ---------------- new: drop sciency words/phrases ----------------
print("Filtering out sciency words")
t0 = time.perf_counter()
phrases = {
    p for p in phrases
    if not is_sciency_phrase(*p.split())
}
t1 = time.perf_counter()
print(f"Filtered sciency terms in {t1 - t0:.2f} seconds")

print(f"Number of Phrases: {len(phrases)}")
t1_total = time.perf_counter()
print(f"Finished in {t1_total - t0_total:.2f} seconds")

output_file = "two_word_phrases.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for p in sorted(phrases):
        f.write(p + "\n")
