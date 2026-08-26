extends Node

const BIOME_DIR := "res://resources/biomes/"
const BASE_SCENE_PATH := "res://scenes/base/base.tscn"

var biomes: Dictionary = {}

func _ready() -> void:
	_load_biomes()

func _load_biomes() -> void:
	var dir := DirAccess.open(BIOME_DIR)
	if dir == null:
		return
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while file_name != "":
		if file_name.ends_with(".tres"):
			var biome: BiomeData = load(BIOME_DIR + file_name)
			biomes[biome.id] = biome
		file_name = dir.get_next()
	dir.list_dir_end()

func get_biome_list() -> Array[BiomeData]:
	var list: Array[BiomeData] = []
	for biome in biomes.values():
		list.append(biome)
	return list

func start_expedition(biome_id: String) -> void:
	if not biomes.has(biome_id):
		return
	var biome: BiomeData = biomes[biome_id]
	GameManager.current_location = biome.id
	SceneTransitionManager.travel_to(biome.scene_path, biome.display_name)

func return_to_base() -> void:
	GameManager.current_location = "Base"
	SceneTransitionManager.travel_to(BASE_SCENE_PATH, "Expedition Base")
