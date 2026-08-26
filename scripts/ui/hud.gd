extends CanvasLayer

@onready var prompt_label: Label = $PromptLabel

func _ready() -> void:
	prompt_label.visible = false
	UIManager.prompt_shown.connect(_on_prompt_shown)
	UIManager.prompt_hidden.connect(_on_prompt_hidden)

func _on_prompt_shown(text: String) -> void:
	prompt_label.text = text
	prompt_label.visible = true

func _on_prompt_hidden() -> void:
	prompt_label.visible = false
