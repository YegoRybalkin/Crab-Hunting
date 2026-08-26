extends RayCast3D

var _current_interactable: Interactable = null

func _physics_process(_delta: float) -> void:
	var collider := get_collider()
	var interactable := collider as Interactable

	if interactable != _current_interactable:
		if _current_interactable:
			UIManager.hide_prompt()
		_current_interactable = interactable
		if _current_interactable:
			UIManager.show_prompt(_current_interactable.prompt_text)

	if _current_interactable and Input.is_action_just_pressed("interact"):
		_current_interactable.interact(owner)
