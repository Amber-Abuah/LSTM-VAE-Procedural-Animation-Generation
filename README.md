## Procedural Animation Generation Using LSTM-VAE
<p align="center">
<img src="https://github.com/user-attachments/assets/633781fc-e97e-4d8c-9fc5-1a635d4f590e" alt="Generated animation preview" width="300"/>
  <br />
  <br />
  Procedurally generate FBX animations efficiently and with a small training set!
</p>

### Workflow
-> Add all FBX training animations into the input_animations directory.  
-> Start Blender and run **bpy_convert_input.py** using the [Blender Development VSCode extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).  
This will import all the FBX animations into blender, record the rotations of each bone and store this data into a text file to be used for training in the next step.  
-> Run **lstm_vae.py** and adjust training parameters as needed.  
Alter sample_outputs to change the number of generated animations outputted.  
The generated animation data will be in the generated_animation_data directory.  
-> Run **bpy_convert_gen_data.py** which will convert the generated data into FBX files.  
Done!🎉 The generated_fbx directory will hold all the generated animations and can be used in any projects, e.g. Unity etc.  
The generated animations should automatically smoothly transition from frame to frame, but feel free to add any post-processing you would like!  

### Notes
- **bpy_convert_input.py** assumes all animations have the same named bones, in the same order. To deal with this, rename similar bones and ensure the bone order when written to and read from a file remain in the exact same order.
- You can use [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to access the Blender Python API for code completion within your IDE.

### Example Detail
The example uses and trains the VAE on animations downloaded from [Mixamo](https://www.mixamo.com).
The dataset only contains 16 animations, yet still produces realistic animations.
