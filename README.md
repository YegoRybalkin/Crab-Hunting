# Crab Hunting

A stylized, lightweight, single-player expedition and progression game about
catching crabs, upgrading a permanent base, and unlocking new biomes.

Built in **Godot 4.3** (GDScript).

## Current status: Phase 1 — Project Foundation

The player can launch the game, load the Base scene, walk around with
mouse-look, sprint, and interact with a placeholder object.

## How to run

1. Install [Godot 4.3](https://godotengine.org/download) (standard, non-.NET build).
2. Open Godot, choose "Import", select this folder's `project.godot`.
3. Press F5 (or the Play button) to run. The Main Menu loads first.

## Controls

| Action | Key |
|---|---|
| Move | W / A / S / D |
| Look | Mouse |
| Sprint | Shift |
| Interact | E |
| Release mouse cursor | Esc |

## Project structure

```
scenes/
  main_menu/    Main menu scene
  base/         Player's permanent base
  player/       Reusable player character scene
scripts/
  core/         Autoload singletons (input setup, UI manager, game manager)
  player/       Player controller
  interaction/  Generic interaction framework (Interactable, InteractionSystem)
  ui/           Screen-specific UI scripts
```

All gameplay content (crabs, equipment, biomes, upgrades) will be added as
data-driven resources in later phases rather than hardcoded into scripts, so
new content doesn't require touching existing gameplay code.

## Roadmap

1. **Project Foundation** *(current)* — base scene, player controller, interaction framework
2. Expedition Framework — world map, helicopter transition, Rocky Coast biome
3. Crab Gameplay — crab AI, catching mechanic, three species
4. Inventory and Economy — carrying capacity, selling, money
5. Equipment Progression — upgrades for catching/exploration/detection/storage
6. Base Progression — upgradeable facilities, decoration slots
7. Research and Collection — crab encyclopedia
8. Save/Load and Polish — persistent, versioned save system
9. Vertical Slice Evaluation
