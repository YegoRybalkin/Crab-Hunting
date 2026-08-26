extends Node

signal prompt_shown(text: String)
signal prompt_hidden
signal expedition_map_requested

func show_prompt(text: String) -> void:
	prompt_shown.emit(text)

func hide_prompt() -> void:
	prompt_hidden.emit()

func open_expedition_map() -> void:
	expedition_map_requested.emit()
