## Game Controller.gd
extends Node

### TODO: Add more words, make a file for all of the word pairs
var word_pairs = ['bake off', 'bake sale', 'bake well', 'bath mat', 'bath mat', 'bath robe', 
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
		"lock jaw", "board state", "mail bag"]

var word_pairs_dict = {}

var player_lives = 3
var player_score = 0

var previous_words = []

var paused = false

func _ready():
	# Key the word dictionary
	key_word_dict()


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
