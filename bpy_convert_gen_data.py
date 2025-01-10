import bpy
import ast
import os

# Converted generated data from VAE to FBX files

animation_max_frames = 100

armature_name = "Armature"
character_model_path = "character_rig/Character.fbx"
generated_anim_path = "generated_animation_data" # Generated rotations as text data (outputted from the VAE)
out_fbx_path = "generated_fbx"

if not os.path.exists(out_fbx_path):
    os.makedirs(out_fbx_path)

# Empty scene
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import rig
bpy.ops.import_scene.fbx(filepath = character_model_path)
scene = bpy.context.scene

files = os.listdir(generated_anim_path)
for anim_file in files:
    print(anim_file)

    # Clear any previous animation
    bpy.data.objects[armature_name].animation_data_clear()

    for action in bpy.data.actions:
        action.use_fake_user = False
        bpy.data.actions.remove(action)


    # Read generated animation data
    with open(generated_anim_path + "/" + anim_file) as f:
        data = ast.literal_eval(f.read())

    bpy.ops.object.mode_set(mode='POSE')

    # Apply rotation data to model and add keyframes
    for f in range(animation_max_frames):
        frame_data = data[f]

        for pose_bone in bpy.data.objects[armature_name].pose.bones:
            x, y, z, w = frame_data.pop(0), frame_data.pop(0), frame_data.pop(0), frame_data.pop(0)
            pose_bone.rotation_mode = 'QUATERNION'
            pose_bone.rotation_quaternion = (w, x, y, z)
            pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=f)

    out_name = anim_file.split(".txt")[0] + ".fbx"
    bpy.ops.export_scene.fbx(filepath=out_fbx_path + "/" + out_name)
    print(f"Animation {anim_file} exported to fbx.")

print(f"All animations exported to fbx at /{out_fbx_path}.")