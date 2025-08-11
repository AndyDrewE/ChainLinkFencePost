## Game Controller.gd
extends Node

### TODO: Add more words, make a file for all of the word pairs
var word_pairs

var word_pairs_dict = {}

var player_lives = 3
var player_score = 0

var previous_words = []

var paused = false

func _ready():
	var file_path = "res://word_pairs_100k.txt" # Adjust path as needed
	word_pairs = load_word_pairs(file_path)
	
	# Key the word dictionary
	key_word_dict()


func load_word_pairs(path: String) -> Array:
	var pairs = []
	var file = FileAccess.open(path, FileAccess.READ)
	if file:
		while not file.eof_reached():
			var line = file.get_line().strip_edges()
			if line != "":
				pairs.append(line)
		file.close()
	return pairs
	
func get_UI_controller() -> Node:
	return get_tree().current_scene.get_node("UIController")

func go_to_start():
	paused = false
	get_tree().change_scene_to_file("res://Scenes/main_menu.tscn")

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
	previous_words.append(word_pairs_dict.keys().pick_random())
	get_UI_controller().create_label(previous_words[-1])
