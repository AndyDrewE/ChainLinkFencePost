## Game Controller.gd
extends Node

var word_pairs = ["bottled water", "water slide", "slide show", "show girl", "girl scout", "scout leader", "leader board", "board game", "game over", "game on", "over easy", "easy bake", "easy living", "bake off", "bake well", "well done", "done for", "off side", "in side", "water softener"]
var word_pairs_dict = {}

func _ready():
	# Key the word dictionary
	key_word_dict()

func key_word_dict():
	for pair in word_pairs:
		var pair_parts = pair.split(" ")
		var key = pair_parts[0]
		if not word_pairs_dict.has(key):
			word_pairs_dict[key] = []
		word_pairs_dict[key].append(pair)

func get_usable_pairs(word):
	return word_pairs_dict.get(word, [])

func is_valid(current_word, previous_word=""):
	if previous_word == "":
		return current_word in word_pairs_dict.keys()
	
	var valid = (previous_word + current_word) in word_pairs
	return valid
