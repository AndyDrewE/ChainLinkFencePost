extends Control

@onready var ui_controller = self.get_parent()

func _on_continue_pressed():
	ui_controller.toggle_pause_menu()


func _on_start_pressed():
	GameController.go_to_start()

func _on_exit_pressed():
	get_tree().quit()

func _on_restart_pressed():
	GameController.paused = false
	get_tree().change_scene_to_file("res://Scenes/main.tscn")
