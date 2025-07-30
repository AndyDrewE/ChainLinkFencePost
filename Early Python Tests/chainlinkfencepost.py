import random as rnd

word_pairs = ["water slide", "slide show", "show girl", "girl scout", "scout leader", "slide deck", "show stopper", "water softener", "leader board", "apple pie", "pie crust"]

def find_available_letters(pairs):
    letters_available = []
    for pair in pairs:
        first_letter = pair.split(" ")[0][0]
        if first_letter not in letters_available:
            letters_available.append(first_letter)
    
    return letters_available

def pick_random_letter(letters):
    num_letters = len(letters)
    rand_index = rnd.randint(0, num_letters - 1)
    return letters[rand_index]

def main():
    current_letters = find_available_letters(word_pairs)
    rand_letter = pick_random_letter(current_letters)
    