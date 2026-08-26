extends CanvasLayer

signal fade_in_finished

@onready var background: ColorRect = $Background
@onready var destination_label: Label = $VBoxContainer/DestinationLabel
@onready var tip_label: Label = $VBoxContainer/TipLabel
@onready var icon_label: Label = $VBoxContainer/IconLabel

var _spin_tween: Tween

func setup(destination_name: String, tip: String) -> void:
	destination_label.text = "Traveling to %s" % destination_name
	tip_label.text = tip
	tip_label.visible = tip != ""

func _ready() -> void:
	background.modulate.a = 0.0
	call_deferred("_center_icon_pivot")
	_start_spin()

	var tween := create_tween()
	tween.tween_property(background, "modulate:a", 1.0, 0.4)
	await tween.finished
	fade_in_finished.emit()

func _center_icon_pivot() -> void:
	icon_label.pivot_offset = icon_label.size / 2.0

func _start_spin() -> void:
	_spin_tween = create_tween().set_loops()
	_spin_tween.tween_property(icon_label, "rotation_degrees", 360.0, 1.5).as_relative()

func fade_out_and_free() -> void:
	if _spin_tween:
		_spin_tween.kill()
	var tween := create_tween()
	tween.tween_property(background, "modulate:a", 0.0, 0.4)
	await tween.finished
	queue_free()
