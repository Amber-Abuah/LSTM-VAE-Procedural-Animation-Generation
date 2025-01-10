import bpy
import os
import shutil 
# Convert input animations to a series of quaternion rotations for the VAE

in_dir = "input_animations" # Original animations to use for training
out_dir = "input_animation_data" # Converted animations stored as .txt
armature_name = "Armature"
animation_max_frames = 100

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

os.makedirs(out_dir)

animations = os.listdir(in_dir)

for anim in animations:
    # Clear scene
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Import FBX animation
    bpy.ops.import_scene.fbx(filepath = in_dir + "/" + anim)
    scene = bpy.context.scene

    data = []

    end_frame = int(bpy.data.objects[armature_name].animation_data.action.curve_frame_range[1]) # Find last frame with keyframe

    # Loop through each frame and record rotation for all bones
    for f in range(scene.frame_start, animation_max_frames + 1):
        scene.frame_set(f)

        # Loop the animation until max frames is reached
        if f > end_frame:
            loop_frame = f % end_frame
            scene.frame_set(loop_frame)

        frame_data = []
        bpy.ops.object.mode_set(mode='POSE')
        
        for pose_bone in bpy.data.objects[armature_name].pose.bones:
            pose_bone.rotation_mode = 'QUATERNION'
            quaternion = pose_bone.rotation_quaternion
            frame_data.extend([quaternion.x, quaternion.y, quaternion.z, quaternion.w])

        data.append(frame_data)

    # Write rotations to text file
    out_name = anim.split(".fbx")[0] + ".txt"
    with open(out_dir + "/" + out_name, "w") as file:
        file.write(str(data))
        print(out_name, "data written to file.")

print("All data written.")

# Optional: export bone order for reference
with open(out_dir + "/BoneOrder.txt", "w") as file:
    for pose_bone in bpy.data.objects[armature_name].pose.bones:
        file.write(pose_bone.name + "\n")

print("Complete.")