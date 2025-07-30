import random as rnd

word_pairs = ["water slide", "slide show", "show girl", "girl scout", "scout leader", "slide deck", "show stopper", "water softener", "leader board", "apple pie", "pie crust"]

def find_nth_words(pairs, n):
    nth_words = []
    for pair in pairs:
        nth_word = pair.split(" ")[n-1]
        if nth_word not in nth_words:
            nth_words.append(nth_word)
    return nth_words



def find_available_letters(words):
    letters_available = []
    for word in words:
        first_letter = word[0]
        if first_letter not in letters_available:
            letters_available.append(first_letter)
    
    return letters_available

def pick_random_letter(letters):
    num_letters = len(letters)
    if num_letters == 1:
        return letters[0]
    
    rand_index = rnd.randint(0, num_letters - 1)
    return letters[rand_index]

def is_valid(current_word, last_word = ""):
    #First time this is checked, the word needs to be check against first_words
    if last_word == "":
        if current_word in find_nth_words(word_pairs, 1):
            return True
        else:
            return False
    
    test_string = last_word + " " + current_word
    if test_string in word_pairs:
        return True
    else:
        return False

def main():
    first_words = find_nth_words(word_pairs, 1)
    current_letters = find_available_letters(first_words)
    rand_letter = pick_random_letter(current_letters)

    current_word = input(rand_letter)
    previous_word = ""

    while is_valid(current_word, previous_word):
        useable_pairs = [pair for pair in word_pairs if pair.split(" ")[0] == current_word]
        print(useable_pairs)
        previous_word = current_word
        current_word = input(rand_letter)


main()