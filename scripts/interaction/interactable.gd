class_name Interactable
extends StaticBody3D

@export var prompt_text: String = "Press E to interact"
@export var interact_message: String = ""

func interact(_player: Node) -> void:
	if interact_message != "":
		print(interact_message)
