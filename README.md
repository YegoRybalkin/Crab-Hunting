# Crab Hunting

A stylized, lightweight, single-player expedition and progression game about
catching crabs, upgrading a permanent base, and unlocking new biomes.

Built in **Godot 4.3** (GDScript).

## Current status: Phase 2 — Expedition Framework

The player can launch the game, load the Base scene, walk around with
mouse-look and sprint, open the Expedition Map by interacting with the
helipad sign, travel to Rocky Coast through a helicopter loading screen,
and return to Base via the extraction point.

Base and Rocky Coast use real (if simple) stylized low-poly models —
character, cabin, equipment room, helipad, signpost, extraction beacon,
and rocks — generated procedurally with Blender rather than primitive
boxes. See `tools/generate_assets.py`.

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
  biomes/       Expedition destinations (Rocky Coast)
  transition/   Helicopter loading screen
  ui/           Expedition map, HUD
  player/       Reusable player character scene
scripts/
  core/         Autoload singletons (input, UI, game state, expeditions, biome data, scene transitions)
  player/       Player controller
  interaction/  Generic interaction framework (Interactable, InteractionSystem)
  ui/           Screen-specific UI scripts
assets/models/  Placeholder-but-real .glb models (characters, base, environment)
tools/          Blender asset-generation pipeline
resources/      Data-driven definitions (biomes today; crabs/equipment/upgrades later)
```

All gameplay content (crabs, equipment, biomes, upgrades) is added as
data-driven resources rather than hardcoded into scripts, so new content
doesn't require touching existing gameplay code.

### Regenerating or extending 3D models

`tools/generate_assets.py` procedurally builds every model in the game via
Blender's Python API and exports each to `assets/models/`. To add a new
asset or tweak an existing one, edit that script, then run (from the repo
root, with Blender installed):

```
blender --background --python tools/generate_assets.py
```

This also renders a preview PNG per asset to `scratch/previews/` (git-ignored)
for a quick visual check before opening Godot.

## Roadmap

1. **Project Foundation** — base scene, player controller, interaction framework
2. **Expedition Framework** *(current)* — world map, helicopter transition, Rocky Coast biome
3. Crab Gameplay — crab AI, catching mechanic, three species
4. Inventory and Economy — carrying capacity, selling, money
5. Equipment Progression — upgrades for catching/exploration/detection/storage
6. Base Progression — upgradeable facilities, decoration slots
7. Research and Collection — crab encyclopedia
8. Save/Load and Polish — persistent, versioned save system
9. Vertical Slice Evaluation
