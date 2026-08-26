import bpy
import bmesh
import math
import os

OUT_MODELS = "assets/models"
OUT_PREVIEWS = "scratch/previews"

os.makedirs(OUT_PREVIEWS, exist_ok=True)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block_collection in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(block_collection):
            if block.users == 0:
                block_collection.remove(block)


def new_material(name, color, roughness=0.9, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def flat_shade(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_flat()
    obj.select_set(False)


def add_box(name, size, location, material, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.data.materials.append(material)
    flat_shade(obj)
    if parent:
        obj.parent = parent
    return obj


def add_cylinder(name, radius, height, location, material, parent=None, vertices=10):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=location, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    flat_shade(obj)
    if parent:
        obj.parent = parent
    return obj


def add_empty(name, location=(0, 0, 0), parent=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
    obj = bpy.context.active_object
    obj.name = name
    if parent:
        obj.parent = parent
    return obj


def make_gable_roof(name, width, depth, roof_height, location, material, parent=None):
    hw, hd = width / 2.0, depth / 2.0
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    v0 = bm.verts.new((-hw, -hd, 0))
    v1 = bm.verts.new((hw, -hd, 0))
    v2 = bm.verts.new((hw, hd, 0))
    v3 = bm.verts.new((-hw, hd, 0))
    v4 = bm.verts.new((0, -hd, roof_height))
    v5 = bm.verts.new((0, hd, roof_height))
    bm.faces.new((v0, v1, v4))
    bm.faces.new((v2, v3, v5))
    bm.faces.new((v1, v2, v5, v4))
    bm.faces.new((v3, v0, v4, v5))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    flat_shade(obj)
    if parent:
        obj.parent = parent
    return obj


def make_lean_to_roof(name, width, depth, low_height, high_height, location, material, parent=None):
    hw, hd = width / 2.0, depth / 2.0
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    v0 = bm.verts.new((-hw, -hd, low_height))
    v1 = bm.verts.new((hw, -hd, low_height))
    v2 = bm.verts.new((hw, hd, high_height))
    v3 = bm.verts.new((-hw, hd, high_height))
    v4 = bm.verts.new((-hw, -hd, 0))
    v5 = bm.verts.new((hw, -hd, 0))
    v6 = bm.verts.new((hw, hd, 0))
    v7 = bm.verts.new((-hw, hd, 0))
    bm.faces.new((v0, v1, v2, v3))
    bm.faces.new((v4, v5, v1, v0))
    bm.faces.new((v5, v6, v2, v1))
    bm.faces.new((v6, v7, v3, v2))
    bm.faces.new((v7, v4, v0, v3))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    flat_shade(obj)
    if parent:
        obj.parent = parent
    return obj


def make_rock(name, radius, location, material, seed, parent=None):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=2, location=location)
    obj = bpy.context.active_object
    obj.name = name
    import random
    rnd = random.Random(seed)
    mesh = obj.data
    for v in mesh.vertices:
        scale_factor = 1.0 + rnd.uniform(-0.28, 0.28)
        v.co.x *= scale_factor
        v.co.y *= scale_factor
        v.co.z *= (1.0 + rnd.uniform(-0.28, 0.28)) * 0.72
        if v.co.z < 0:
            v.co.z *= 0.3
    obj.scale = (1, 1, 1)
    mesh.update()
    obj.data.materials.append(material)
    flat_shade(obj)
    if parent:
        obj.parent = parent
    return obj


def get_all_children(root):
    result = [root]
    for child in root.children:
        result.extend(get_all_children(child))
    return result


def export_glb(root, filepath):
    objs = get_all_children(root)
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = root
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_yup=True,
        export_apply=True,
    )
    print("EXPORTED:", filepath)


def setup_ground_and_world():
    bpy.context.scene.world = bpy.data.worlds.new("World")
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.75, 0.82, 0.88, 1.0)
    bg.inputs[1].default_value = 1.0

    ground_mat = new_material("GroundPreview", (0.55, 0.58, 0.5), roughness=1.0)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "PreviewGround"
    ground.data.materials.append(ground_mat)
    return ground


def render_preview(filename, cam_pos, cam_target, resolution=640, samples=48):
    scene = bpy.context.scene
    bpy.ops.object.camera_add(location=cam_pos)
    cam = bpy.context.active_object
    direction = (
        cam_target[0] - cam_pos[0],
        cam_target[1] - cam_pos[1],
        cam_target[2] - cam_pos[2],
    )
    import mathutils
    quat = mathutils.Vector(direction).to_track_quat("-Z", "Y")
    cam.rotation_euler = quat.to_euler()
    scene.camera = cam

    sun_data = bpy.data.lights.new("Sun", type="SUN")
    sun_data.energy = 1.8
    sun_data.angle = 0.2
    sun = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(55), 0, math.radians(35))

    fill_data = bpy.data.lights.new("Fill", type="SUN")
    fill_data.energy = 0.5
    fill = bpy.data.objects.new("Fill", fill_data)
    bpy.context.collection.objects.link(fill)
    fill.rotation_euler = (math.radians(110), 0, math.radians(-120))

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    scene.view_settings.view_transform = "Standard"
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.filepath = os.path.join(OUT_PREVIEWS, filename)
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", scene.render.filepath)

    bpy.data.objects.remove(cam, do_unlink=True)
    bpy.data.objects.remove(sun, do_unlink=True)
    bpy.data.objects.remove(fill, do_unlink=True)


def remove_all_except_ground():
    ground = bpy.data.objects.get("PreviewGround")
    for obj in list(bpy.data.objects):
        if obj is not ground:
            bpy.data.objects.remove(obj, do_unlink=True)


# ---------------------------------------------------------------------------

def build_crab_hunter():
    root = add_empty("CrabHunter")

    skin = new_material("Skin", (0.85, 0.65, 0.5))
    jacket = new_material("Jacket", (0.82, 0.42, 0.14))
    pants = new_material("Pants", (0.28, 0.26, 0.36))
    boots = new_material("Boots", (0.22, 0.14, 0.08))
    hat = new_material("Hat", (0.22, 0.28, 0.18))
    pack = new_material("Pack", (0.35, 0.25, 0.12))

    add_box("LegL", (0.16, 0.18, 0.8), (-0.11, 0, 0.4), pants, root)
    add_box("LegR", (0.16, 0.18, 0.8), (0.11, 0, 0.4), pants, root)
    add_box("BootL", (0.18, 0.24, 0.16), (-0.11, 0.02, 0.08), boots, root)
    add_box("BootR", (0.18, 0.24, 0.16), (0.11, 0.02, 0.08), boots, root)

    add_box("Torso", (0.46, 0.28, 0.58), (0, 0, 1.09), jacket, root)
    add_box("Backpack", (0.32, 0.14, 0.4), (0, -0.2, 1.12), pack, root)

    add_box("ArmL", (0.14, 0.14, 0.52), (-0.32, 0, 1.06), jacket, root)
    add_box("ArmR", (0.14, 0.14, 0.52), (0.32, 0, 1.06), jacket, root)
    add_box("HandL", (0.15, 0.15, 0.13), (-0.32, 0, 0.75), skin, root)
    add_box("HandR", (0.15, 0.15, 0.13), (0.32, 0, 0.75), skin, root)

    add_box("Head", (0.3, 0.3, 0.32), (0, 0, 1.56), skin, root)
    add_box("HatBrim", (0.4, 0.4, 0.05), (0, 0, 1.735), hat, root)
    add_box("HatTop", (0.28, 0.28, 0.14), (0, 0, 1.83), hat, root)

    return root


def build_cabin():
    root = add_empty("Cabin")

    wall_mat = new_material("CabinWall", (0.55, 0.36, 0.2))
    roof_mat = new_material("CabinRoof", (0.32, 0.18, 0.14))
    door_mat = new_material("CabinDoor", (0.3, 0.18, 0.08))
    window_mat = new_material("CabinWindow", (0.55, 0.75, 0.8), roughness=0.2)

    add_box("Walls", (4.0, 4.0, 2.6), (0, 0, 1.3), wall_mat, root)
    make_gable_roof("Roof", 4.6, 4.6, 1.4, (0, 0, 2.6), roof_mat, root)
    add_box("Door", (0.8, 0.08, 1.7), (0, -2.02, 0.85), door_mat, root)
    add_box("WindowL", (0.6, 0.08, 0.6), (-1.3, -2.02, 1.5), window_mat, root)
    add_box("WindowR", (0.6, 0.08, 0.6), (1.3, -2.02, 1.5), window_mat, root)

    return root


def build_equipment_room():
    root = add_empty("EquipmentRoom")

    wall_mat = new_material("EquipWall", (0.5, 0.52, 0.56))
    roof_mat = new_material("EquipRoof", (0.35, 0.37, 0.4))
    door_mat = new_material("EquipDoor", (0.2, 0.55, 0.55))
    tank_mat = new_material("EquipTank", (0.75, 0.3, 0.2))

    add_box("Walls", (3.2, 3.2, 2.2), (0, 0, 1.1), wall_mat, root)
    make_lean_to_roof("Roof", 3.6, 3.6, 0.3, 0.9, (0, 0, 2.2), roof_mat, root)
    add_box("Door", (1.0, 0.08, 1.7), (0, -1.62, 0.85), door_mat, root)
    add_cylinder("Tank", 0.35, 1.4, (1.9, -1.5, 0.7), tank_mat, root, vertices=12)

    return root


def build_rock_cluster(name, seed_base):
    root = add_empty(name)
    rock_mat = new_material(name + "Mat", (0.32, 0.3, 0.28))
    make_rock(name + "_A", 0.9, (0, 0, 0.55), rock_mat, seed_base, root)
    make_rock(name + "_B", 0.5, (0.7, 0.4, 0.3), rock_mat, seed_base + 1, root)
    make_rock(name + "_C", 0.35, (-0.5, 0.5, 0.2), rock_mat, seed_base + 2, root)
    return root


def build_signpost():
    root = add_empty("Signpost")
    post_mat = new_material("SignPost", (0.35, 0.24, 0.14))
    board_mat = new_material("SignBoard", (0.85, 0.75, 0.5))

    add_cylinder("Post", 0.06, 1.6, (0, 0, 0.8), post_mat, root, vertices=8)
    add_box("Board", (0.7, 0.06, 0.5), (0, 0, 1.5), board_mat, root)

    return root


def build_extraction_beacon():
    root = add_empty("ExtractionBeacon")
    base_mat = new_material("BeaconBase", (0.25, 0.25, 0.28))
    pole_mat = new_material("BeaconPole", (0.9, 0.55, 0.15))
    light_mat = new_material("BeaconLight", (1.0, 0.35, 0.1))

    add_cylinder("Base", 0.9, 0.12, (0, 0, 0.06), base_mat, root, vertices=16)
    add_cylinder("Pole", 0.06, 1.6, (0, 0, 0.86), pole_mat, root, vertices=8)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.18, subdivisions=2, location=(0, 0, 1.72))
    orb = bpy.context.active_object
    orb.name = "Light"
    orb.data.materials.append(light_mat)
    flat_shade(orb)
    orb.parent = root

    return root


def build_helipad():
    root = add_empty("Helipad")
    pad_mat = new_material("PadSurface", (0.2, 0.2, 0.22))
    mark_mat = new_material("PadMark", (0.9, 0.85, 0.2))

    add_cylinder("Pad", 3.5, 0.2, (0, 0, 0.1), pad_mat, root, vertices=20)
    add_box("MarkLeft", (0.3, 1.6, 0.02), (-0.55, 0, 0.21), mark_mat, root)
    add_box("MarkRight", (0.3, 1.6, 0.02), (0.55, 0, 0.21), mark_mat, root)
    add_box("MarkBar", (1.4, 0.3, 0.02), (0, 0, 0.21), mark_mat, root)

    return root


ASSETS = [
    ("crab_hunter", build_crab_hunter, "characters", (2.2, -2.6, 1.8), (0, 0, 0.9)),
    ("cabin", build_cabin, "base", (7.5, -8.5, 3.2), (0, 0, 1.6)),
    ("equipment_room", build_equipment_room, "base", (6.0, -6.5, 2.6), (0, 0, 1.2)),
    ("helipad", build_helipad, "base", (5.5, -5.5, 3.0), (0, 0, 0)),
    ("signpost", build_signpost, "base", (2.2, -2.4, 1.6), (0, 0, 0.9)),
    ("extraction_beacon", build_extraction_beacon, "environment", (2.6, -2.8, 1.9), (0, 0, 1.0)),
    ("rock_a", lambda: build_rock_cluster("RockClusterA", 1), "environment", (2.6, -2.8, 1.4), (0, 0, 0.4)),
    ("rock_b", lambda: build_rock_cluster("RockClusterB", 10), "environment", (2.6, -2.8, 1.4), (0, 0, 0.4)),
    ("rock_c", lambda: build_rock_cluster("RockClusterC", 20), "environment", (2.6, -2.8, 1.4), (0, 0, 0.4)),
]

clear_scene()
setup_ground_and_world()

for asset_name, builder, subfolder, cam_pos, cam_target in ASSETS:
    remove_all_except_ground()
    root = builder()
    glb_path = os.path.join(OUT_MODELS, subfolder, asset_name + ".glb")
    export_glb(root, glb_path)
    render_preview(asset_name + ".png", cam_pos, cam_target)
    if asset_name == "crab_hunter":
        render_preview("crab_hunter_side.png", (3.0, 0, 1.2), (0, 0, 1.0))

print("ALL_DONE")
