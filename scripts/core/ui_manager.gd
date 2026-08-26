extends Node

signal prompt_shown(text: String)
signal prompt_hidden

func show_prompt(text: String) -> void:
	prompt_shown.emit(text)

func hide_prompt() -> void:
	prompt_hidden.emit()
