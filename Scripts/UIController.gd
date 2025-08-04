extends Control


@onready var player_input_textbox = $PlayerInput
@onready var previous_words = $PreviousWordsBox

var previous_word = ""



func create_label(label_text):
	var new_label = Label.new()
	new_label.text = label_text
	new_label.add_theme_font_size_override("font_size", 48)
	previous_words.add_child(new_label)
	previous_word = label_text

func flash_label_invalid():
	var original_color = player_input_textbox.modulate
	player_input_textbox.modulate = Color.RED

	var tween = get_tree().create_tween()
	tween.tween_property(player_input_textbox, "modulate", original_color, 0.5) # 0.5 sec


func _on_player_input_text_submitted(new_text):
	if GameController.is_valid(new_text, previous_word):
		create_label(new_text)
		#Erase Text
		player_input_textbox.text = ""
	else:
		flash_label_invalid()
