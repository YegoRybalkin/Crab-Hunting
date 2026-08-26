extends Area3D

@export var detection_radius: float = 3.5

@onready var _shape: CollisionShape3D = $CollisionShape3D

var _nearby: Array[Interactable] = []
var _current_interactable: Interactable = null

func _ready() -> void:
	collision_layer = 0
	collision_mask = 4
	if _shape.shape is SphereShape3D:
		(_shape.shape as SphereShape3D).radius = detection_radius
	area_entered.connect(_on_area_entered)
	area_exited.connect(_on_area_exited)

func _on_area_entered(area: Area3D) -> void:
	var interactable := area as Interactable
	if interactable:
		_nearby.append(interactable)

func _on_area_exited(area: Area3D) -> void:
	var interactable := area as Interactable
	if interactable:
		_nearby.erase(interactable)

func _physics_process(_delta: float) -> void:
	var closest: Interactable = null
	var closest_dist := INF
	for interactable in _nearby:
		var dist := global_position.distance_to(interactable.global_position)
		if dist < closest_dist:
			closest_dist = dist
			closest = interactable

	if closest != _current_interactable:
		_current_interactable = closest
		if _current_interactable:
			UIManager.show_prompt(_current_interactable.prompt_text)
		else:
			UIManager.hide_prompt()

	if _current_interactable and Input.is_action_just_pressed("interact"):
		_current_interactable.interact(owner)
