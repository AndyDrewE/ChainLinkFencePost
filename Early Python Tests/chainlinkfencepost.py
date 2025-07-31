import random as rnd
from collections import defaultdict

with open("two_word_phrases.txt", "r") as f:
    phrases = [line.strip().lower() for line in f]

index = defaultdict(list)
for p in phrases:
    first, second = p.split(" ")
    index[first].append(p)


def find_nth_words(pairs, n):
    return list({pair.split()[n-1] for pair in pairs})


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

def get_usable_pairs(word):
    return index.get(word, [])

def is_valid(current_word, previous_word=""):
    if previous_word == "":
        return current_word in first_words_set
    return f"{previous_word} {current_word}" in phrases_set


def main():
    distinct_words = set(first_words + second_words)
    current_letters = find_available_letters(first_words)
    rand_letter = pick_random_letter(current_letters)

    current_word = (rand_letter + input(rand_letter)).lower()
    previous_word = ""

    while is_valid(current_word, previous_word):
        useable_pairs = get_usable_pairs(current_word)
        # print(f"DEBUG: Looking for pairs starting with '{current_word}'")
        print(f"DEBUG: Found {len(useable_pairs)} matches")   
        if useable_pairs:
            second_words_usable = find_nth_words(useable_pairs, 2)
            current_letters = find_available_letters(second_words_usable)
            rand_letter = pick_random_letter(current_letters)
            previous_word = current_word
            current_word = rand_letter + input(rand_letter)
        else: 
            print("No valid next word")
            break
    print("End of Game")


first_words = find_nth_words(phrases, 1)
second_words = find_nth_words(phrases, 2)
first_words_set = set(first_words)
phrases_set = set(phrases)

main()