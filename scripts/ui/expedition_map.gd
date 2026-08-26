extends Control

const BIOME_ENTRY_SCENE: PackedScene = preload("res://scenes/ui/biome_entry.tscn")

@onready var biome_list_container: VBoxContainer = $Panel/VBoxContainer/BiomeList
@onready var close_button: Button = $Panel/VBoxContainer/CloseButton

func _ready() -> void:
	visible = false
	UIManager.expedition_map_requested.connect(_on_map_requested)
	close_button.pressed.connect(_on_close_pressed)
	_populate()

func _populate() -> void:
	for child in biome_list_container.get_children():
		child.queue_free()
	for biome in ExpeditionManager.get_biome_list():
		var entry := BIOME_ENTRY_SCENE.instantiate()
		biome_list_container.add_child(entry)
		entry.setup(biome)
		entry.expedition_started.connect(_on_expedition_started)

func _on_map_requested() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _on_close_pressed() -> void:
	visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _on_expedition_started(biome_id: String) -> void:
	visible = false
	ExpeditionManager.start_expedition(biome_id)
