extends Control


@onready var player_input_textbox = $PlayerInput
@onready var previous_words = $PreviousWordsBox


func create_label(label_text):
	var new_label = Label.new()
	new_label.text = label_text
	new_label.add_theme_font_size_override("font_size", 48)
	previous_words.add_child(new_label)


func _on_player_input_text_submitted(new_text):
	create_label(new_text)
	
	#Erase Text
	player_input_textbox.text = ""
