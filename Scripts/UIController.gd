extends Control

#Player Input Variables
@onready var player_input_textbox = $PlayerInput
@onready var previous_words = $PreviousWordsBox

#Stats Box variables
@onready var num_lives_label = $StatsBox/Lives/NumLives
@onready var score_label = $StatsBox/Score/ScoreLabel

#GameOver
@onready var game_over_label = $GameOver


func _ready():
	update_stats_box()
	
	#Pick first word and add it to the previous words box
	GameController.pick_first_word()

## Update all in the stats box
func update_stats_box():
	update_lives_label()
	update_score_label()

func update_lives_label():
	num_lives_label.text = "%d" % GameController.player_lives

func update_score_label():
	score_label.text = "%d" % GameController.player_score

#Creates label for previous words to display
func create_label(label_text):
	var new_label = Label.new()
	new_label.text = label_text
	new_label.add_theme_font_size_override("font_size", 48)
	previous_words.add_child(new_label)

func flash_label_invalid():
	var original_color = player_input_textbox.modulate
	player_input_textbox.modulate = Color.RED

	var tween = get_tree().create_tween()
	tween.tween_property(player_input_textbox, "modulate", original_color, 0.5) # 0.5 sec

func game_over():
	game_over_label.visible = true
	player_input_textbox.editable = false

func _on_player_input_text_submitted(new_text):
	if player_input_textbox.editable:
		new_text = new_text.to_lower()
		if GameController.is_valid(new_text, GameController.previous_word):
			create_label(new_text)
			GameController.previous_word = new_text
			#Erase Text
			player_input_textbox.text = ""
			
			#Add however long the word is to score
			GameController.update_score(len(new_text))
		else:
			flash_label_invalid()
			#Take away a life
			GameController.update_lives(-1)
