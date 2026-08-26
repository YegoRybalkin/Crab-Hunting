class_name Interactable
extends Area3D

@export var prompt_text: String = "Press E to interact"
@export var interact_message: String = ""

func _ready() -> void:
	collision_layer = 4
	collision_mask = 0

func interact(_player: Node) -> void:
	if interact_message != "":
		print(interact_message)
