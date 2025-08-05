## Game Controller.gd
extends Node

var word_pairs = ["chain link", "chain mail", "fence post", "link fence", "mail room", "bed room", "guest bed", "bath room", "bath mat", "post office", "office space", "office building", "building manager", "general manager", "bottled water", "water slide", "slide show", "show girl", "girl scout", "scout leader", "leader board", "board game", "game over", "game on", "over easy", "easy bake", "easy living", "bake off", "bake well", "well done", "done for", "off side", "in side", "water softener"]
var word_pairs_dict = {}

var player_lives = 3
var player_score = 0

var previous_word = ""

func _ready():
	# Key the word dictionary
	key_word_dict()


func get_UI_controller() -> Node:
	return get_tree().current_scene.get_node("UIController")

func key_word_dict():
	for pair in word_pairs:
		var pair_parts = pair.split(" ")
		var key = pair_parts[0]
		if not word_pairs_dict.has(key):
			word_pairs_dict[key] = []
		word_pairs_dict[key].append(pair)

func get_usable_pairs(word):
	return word_pairs_dict.get(word, [])

func is_valid(current_word, previous=""):
	#print("Previous Word: " + previous_word)
	#print("Current Word: " + current_word)
	
	if previous == "":
		return current_word in word_pairs_dict.keys()
	
	var valid = (previous + " " + current_word) in word_pairs
	#print(valid)
	return valid

func update_lives(cost):
	player_lives += cost
	get_UI_controller().update_lives_label()
	
	if player_lives == 0:
		get_UI_controller().game_over()

func update_score(cost):
	player_score += cost
	get_UI_controller().update_score_label()

func pick_first_word():
	previous_word = word_pairs_dict.keys().pick_random()
	get_UI_controller().create_label(previous_word)
