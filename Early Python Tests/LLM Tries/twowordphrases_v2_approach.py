# make_word_pairs.py
# Generate ~100,000 natural two-word collocations (adj+noun, noun+noun)
# tuned for ~8th-grade readability and your filtering rules.

import re
import random
import sys
from pathlib import Path
from collections import defaultdict

# ---- Config ----
TARGET_COUNT = 40_000
OUTPUT_PATH = Path("word_pairs_40k.txt")

# Frequency thresholds (Zipf scale ~ 1..7)
# Higher = more common. Tune for readability.
ZIPF_MIN_WORD = 5.2       # individual word must be fairly common
ZIPF_MIN_BIGRAM = 4.7      # bigram must be common enough to sound natural

# Candidate pool sizes (bigger = slower, but better coverage)
TOP_WORDS = 120_000        # start from the 120k most common English words (wordfreq)
MAX_NOUNS = 18_000         # cap nouns kept after POS-filter
MAX_ADJS  = 8_000          # cap adjectives kept after POS-filter

# Randomness for variety
RANDOM_SEED = 42

# ---- Seed pairs (must include even if they violate strict patterns) ----
SEED_PAIRS = [
'bake off', 'bake sale', 'bake well', 'bath mat', 'bath mat', 'bath robe',  'bath room', 'bath salts', 'bath sponge', 'bath towel', 'bed room', 'black belt',
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
 "lock jaw", "board state", "mail bag"
]

# ---- Imports that need installation ----
try:
    import spacy
except ImportError:
    sys.exit("Please install spaCy: pip install spacy && python -m spacy download en_core_web_sm")

try:
    from wordfreq import top_n_list, zipf_frequency
except ImportError:
    sys.exit("Please install wordfreq: pip install wordfreq")

try:
    from better_profanity import profanity
except ImportError:
    sys.exit("Please install better_profanity: pip install better_profanity")

# ---- Init ----
random.seed(RANDOM_SEED)
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])
profanity.load_censor_words()

ALPHA_RE = re.compile(r"^[a-z]{2,}$")  # lowercase alphabetic, min len 2

# British spellings to exclude (common ones); prefer American
BRIT_EXCLUDE = {
    "colour","favourite","flavour","honour","labour","neighbour","rumour",
    "centre","theatre","metre","litre","kilometre","tyre","aluminium","cheque",
    "catalogue","dialogue","monologue","travelling","grey","defence","offence",
    "licence","practise","realise","organise","analyse","apologise","pyjamas"
}

# Brand-ish and technical-ish stoplists (kept small and conservative)
BRANDS = {
    "google","amazon","microsoft","apple","netflix","spotify","coca","pepsi","nike",
    "adidas","samsung","tiktok","instagram","facebook","meta","intel","amd","nvidia",
    "tesla","uber","lyft","starbucks","mcdonalds","disney","hulu","oracle","ibm"
}
TECH_TERMS = {
    "quantum","neural","neuron","synapse","nucleus","molecule","protein","enzyme",
    "genome","chromosome","dataset","database","algorithm","binary","cryptography",
    "crypto","blockchain","compile","syntax","runtime","protocol","nanotech",
    "isotope","vector","matrix","calculus","physics","chemistry","biology","geology",
    "astronomy","astrophysics","thermodynamics","electric","circuit","voltage",
    "current","frequency","spectrum","quantify","molecule","atomic","ionic","covalent"
}

# Some “too formal/Latinate” filters to bias toward 8th‑grade vocabulary
LATIN_GREEK_SUFFIXES = (
    "ology","nomy","philia","phobia","phile","metry","graphy","gamy","genic",
    "genics","pharm","sophy","sophy","sophy","tion","sion","ment","ance","ence"
)

def is_simple_word(w: str) -> bool:
    return (
        ALPHA_RE.match(w) is not None and
        w not in BRIT_EXCLUDE and
        w not in BRANDS and
        not any(w.endswith(suf) for suf in LATIN_GREEK_SUFFIXES) and
        zipf_frequency(w, "en") >= ZIPF_MIN_WORD and
        not profanity.contains_profanity(w)
    )

def is_ok_pair(a: str, b: str) -> bool:
    if not (is_simple_word(a) and is_simple_word(b)):
        return False
    # no exact duplicates, hyphens blocked by regex, already lowercase
    phrase = f"{a} {b}"
    # favor natural collocations by requiring a minimum bigram frequency
    if zipf_frequency(phrase, "en") < ZIPF_MIN_BIGRAM:
        return False
    # lightly exclude technical flavor if either word is in TECH_TERMS
    if a in TECH_TERMS or b in TECH_TERMS:
        return False
    return True

def pos_filter(words):
    """Tag with spaCy and return nouns and adjectives only."""
    nouns, adjs = [], []
    # Batch for speed
    for doc in nlp.pipe(words, batch_size=5000):
        for token in doc:
            t = token.text
            # SpaCy POS: NOUN/PROPN/ADJ
            if token.pos_ == "NOUN":  # exclude PROPN (proper nouns)
                nouns.append(t)
            elif token.pos_ == "ADJ":
                adjs.append(t)
    # Dedup while keeping order
    def dedup(seq):
        seen = set()
        out = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out
    return dedup(nouns), dedup(adjs)

def main():
    print("Building candidate vocabulary from wordfreq…")
    vocab = [w for w in top_n_list("en", n=TOP_WORDS) if w.islower()]
    # keep only alphabetic and simple words with decent frequency
    vocab = [w for w in vocab if ALPHA_RE.match(w) and zipf_frequency(w, "en") >= ZIPF_MIN_WORD]
    # remove british spellings early
    vocab = [w for w in vocab if w not in BRIT_EXCLUDE]

    print(f"POS-tagging ~{len(vocab)} words with spaCy to find nouns and adjectives…")
    nouns, adjs = pos_filter(vocab)

    # cap sizes to keep run-time reasonable
    nouns = nouns[:MAX_NOUNS]
    adjs  = adjs[:MAX_ADJS]

    print(f"Kept {len(nouns)} nouns and {len(adjs)} adjectives.")

    rng = random.Random(RANDOM_SEED)

    results = set()

    # 1) Start with noun–noun pairs (sampled)
    print("Generating noun–noun candidates and scoring…")
    # Prefer heads that often form compounds (high-frequency general nouns)
    top_heads = nouns[: min(6000, len(nouns))]
    top_tails = nouns[: min(12000, len(nouns))]

    # Sample combinations to avoid full Cartesian blowup
    attempts = 0
    target_noun_noun = TARGET_COUNT // 2
    while len(results) < target_noun_noun and attempts < target_noun_noun * 30:
        a = rng.choice(top_heads)
        b = rng.choice(top_tails)
        attempts += 1
        if a == b:
            continue
        if is_ok_pair(a, b):
            results.add(f"{a} {b}")
    print(f"Selected {len(results)} noun–noun pairs after {attempts} attempts.")

    # 2) Adjective–noun pairs
    print("Generating adjective–noun candidates and scoring…")
    target_adj_noun = TARGET_COUNT - len(results)
    attempts = 0
    while len(results) < TARGET_COUNT and attempts < target_adj_noun * 40:
        a = rng.choice(adjs)
        b = rng.choice(nouns)
        attempts += 1
        if is_ok_pair(a, b):
            results.add(f"{a} {b}")
    print(f"Total pairs after adj+noun: {len(results)} from {attempts} attempts in this phase.")

    # 3) Include seeds verbatim (even if not adj+noun or noun+noun)
    print("Adding required seed pairs…")
    for s in SEED_PAIRS:
        s = s.lower().strip()
        # enforce lowercase and alphabetic tokens separated by a space
        parts = s.split()
        if len(parts) == 2 and all(ALPHA_RE.match(p) for p in parts):
            # try to keep only if it doesn't violate profanity/brand filters
            if not profanity.contains_profanity(s) and all(p not in BRANDS for p in parts):
                results.add(s)
        else:
            # If a seed contains non-alphabetic or multiple spaces (“runner up”, “upside down”), 
            # we still include to honor your requirement—append at the end, normalized to spaces.
            # You can comment this branch out if you want to enforce strict two-alpha-word rule.
            results.add(" ".join(parts))

    # Finalize
    pairs = sorted(results)  # stable order; remove sort() if you prefer random order
    print(f"Final count: {len(pairs)}")

    # Write file: one pair per line, lowercase
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for p in pairs:
            f.write(p + "\n")

    print(f"Wrote {len(pairs)} pairs to {OUTPUT_PATH.resolve()}")

if __name__ == "__main__":
    main()
