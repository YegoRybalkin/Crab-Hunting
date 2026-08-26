extends Node

const HELICOPTER_TRANSITION_SCENE: PackedScene = preload("res://scenes/transition/helicopter_transition.tscn")
const MIN_DISPLAY_MS := 1200

const TIPS: Array[String] = [
	"Different crabs prefer different habitats -- explore thoroughly.",
	"Your carrying capacity is limited -- choose your catches wisely.",
	"Return to base regularly to sell loot and upgrade your gear.",
]

func travel_to(scene_path: String, destination_name: String) -> void:
	var transition: CanvasLayer = HELICOPTER_TRANSITION_SCENE.instantiate()
	get_tree().root.add_child(transition)
	transition.setup(destination_name, TIPS.pick_random())
	await transition.fade_in_finished

	var start_time := Time.get_ticks_msec()
	ResourceLoader.load_threaded_request(scene_path)
	while ResourceLoader.load_threaded_get_status(scene_path) != ResourceLoader.THREAD_LOAD_LOADED:
		await get_tree().process_frame

	var elapsed_ms := Time.get_ticks_msec() - start_time
	var remaining_ms := MIN_DISPLAY_MS - elapsed_ms
	if remaining_ms > 0:
		await get_tree().create_timer(remaining_ms / 1000.0).timeout

	var next_scene: PackedScene = ResourceLoader.load_threaded_get(scene_path)
	get_tree().change_scene_to_packed(next_scene)

	await transition.fade_out_and_free()
