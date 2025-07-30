word_pairs = ["water slide", "slide show", "show girl", "girl scout", "scout leader", "slide deck", "show stopper", "water softener", "leader board", "apple pie", "pie crust"]

def extract_first_words(pairs):
    for pair in pairs:
        print(pair.split(" ")[0][0])

extract_first_words(word_pairs)