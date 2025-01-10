## Procedural Animation Generation Using LSTM-VAE
<p align="center">
<img src="https://github.com/user-attachments/assets/633781fc-e97e-4d8c-9fc5-1a635d4f590e" alt="Walking" height="300"/>
<img src="https://github.com/user-attachments/assets/be409be6-9d00-49aa-aa03-11ec076042cf" alt="Sitting" height="300"/>
<img src="https://github.com/user-attachments/assets/a370faca-32b0-4541-990a-c1857c5b9564" alt="Dancing" height="300"/>




  
  <br />
  Procedurally generate FBX animations efficiently with small training sets!
</p>

### Workflow
-> Add all FBX training animations into the _input_animations_ directory.  
-> Start Blender and run **bpy_convert_input.py** using the [Blender Development VSCode extension](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).  
This will import all the FBX animations into Blender, record the rotations of each bone and store this data into a text file to be used for training in the next step.  
-> Run **lstm_vae.py** and adjust training parameters as needed.  
Alter _sample_outputs_ if you wish to change the number of generated animations outputted.  
The generated animation data will be in the _generated_animation_data_ directory.  
-> Run **bpy_convert_gen_data.py** which will convert the generated data into FBX files.  
Done! 🎉 The generated_fbx directory will hold all the generated animations and can be used in any projects, e.g. Unity etc.  
The generated animations should automatically smoothly transition from frame to frame, but feel free to add any post-processing you would like!  

### Notes
- **bpy_convert_input.py** assumes all animations have the same named bones, in the same order. To deal with this, rename similar bones and ensure the bone order when written to and read from a file remain in the exact same order.
- You can use [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to access the Blender Python API for code completion within your IDE.
- Ensure that _animation_max_frames_ in **bpy_convert_input.py** and **bpy_convert_gen_data.py** and _seq_length_ in **lstm_vae.py** all have the same value.

#### Folder Structure
- _character_rig_ contains the rigged model for the generated animations to be applied to.
- _generated_animation_data_ contains the generated animation data as a series of rotations for each bone.
- _generated_fbx_ contains the generated animations as FBX files which can be used in other software etc.
- _input_animation_data_ contains the training animation data as a series of rotations.
- _input_animations_ contains the set of FBX animations to be used to train the VAE.

### Example Details
The example uses and trains the VAE on animations downloaded from [Mixamo](https://www.mixamo.com/#/).  
Mixamo Animation download settings:  
-> _Format: FBX Binary_  
-> _Skin: Without Skin_  
-> _Frames per Second: 30_  
-> _Keyframe Reduction: None_  
  
The training dataset only contains 16 animations, yet still produces realistic animations.  
The sitting and dancing animations only used 7 animations each, additionally.   

### Model Architecture
**Encoder:** 2 layered LSTM  
**Decoder:** 2 layered LSTM  
**Mean and Var:** 1 Fully Connected Layer  
**Optimiser:** Adam  
