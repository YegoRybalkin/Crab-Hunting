extends PanelContainer

signal expedition_started(biome_id: String)

@onready var name_label: Label = $VBoxContainer/NameLabel
@onready var info_label: Label = $VBoxContainer/InfoLabel
@onready var start_button: Button = $VBoxContainer/StartButton

var _biome_id: String = ""

func setup(biome: BiomeData) -> void:
	_biome_id = biome.id
	name_label.text = biome.display_name
	info_label.text = "Difficulty: %s   Conditions: %s   Crabs: %s" % [
		biome.difficulty, biome.environmental_conditions, ", ".join(biome.possible_crabs)
	]
	start_button.disabled = not biome.unlocked
	start_button.text = "Start Expedition" if biome.unlocked else "Locked"
	start_button.pressed.connect(_on_start_pressed)

func _on_start_pressed() -> void:
	expedition_started.emit(_biome_id)
