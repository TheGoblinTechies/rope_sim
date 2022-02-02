"""
Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.

Assimp Loading
------------
- Loads a handful of MJCF and URDF assets using assimp to load their meshes
- Demonstrates the usage of `use_mesh_materials` to
  override materials specified in asset files with mesh textures/materials
"""
# system import
import os
import math
import numpy as np
from numpy.core.defchararray import index
from PIL import Image as im



# isaac gym import
from isaacgym import gymutil
from isaacgym import gymapi
from isaacgym import gymtorch
import torch

# For easier readign
from load_all import *
from init import *
from apply_force import *
from make_dir import *
from texture import *

#########################
# Processing argparse
#########################
from args_prepare import *
print('env_num_bodies', env_num_bodies)

#########################
# Load useful objects
#########################

# See load_all.py

# # Here a trick to set segmentationId is:
# # set rope to 1,2,...
# # set all other object to 0 as well as walls and the ground
# obj_handle = {}

# for i in range(len(asset_descriptors)):
#     obj_handle[obj_namelist[i]] = gym.create_actor(env, assets[i],
#                                                    asset_descriptors[i].asset_pose,
#                                                    asset_descriptors[i].asset_name,
#                                                    group=0,
#                                                    filter=0,
#                                                    segmentationId=1 if asset_descriptors[i].asset_type=="core" else 0)
#     gym.set_actor_scale(env, obj_handle[obj_namelist[i]], asset_descriptors[i].asset_scaling)


#########################
# Load textures for objects
#########################

# Load textures from file. Loads all .jpgs from the specified directory as textures
# DR_MODULAR_MARK
# texture_files = os.listdir("../../assets/textures/blender/")
# texture_handles = []
# for file in texture_files:
#     if file.endswith(".jpg") or file.endswith(".png"):
#         h = gym.create_texture_from_file(sim, os.path.join("../../assets/textures/blender/", file))
#         if h == gymapi.INVALID_HANDLE:
#             print("Couldn't load texture %s" % file)
#         else:
#             texture_handles.append(h)

texture_files = os.listdir("../../assets/textures/")
texture_handles = []
for file in texture_files:
    if file.endswith(".jpg") or file.endswith(".png"):
        h = gym.create_texture_from_file(sim, os.path.join("../../assets/textures/", file))
        if h == gymapi.INVALID_HANDLE:
            print("Couldn't load texture %s" % file)
        else:
            texture_handles.append(h)


# Load textures for walls

for i in range(len(asset_descriptors)):
    if asset_descriptors[i].asset_type != "core":
        actor_handle = obj_handle[asset_descriptors[i].asset_name]
        # DR_MODULAR_MARK
        painted_texture_idx = np.random.randint(len(texture_handles)-1,size=1)[0]
        gym.set_rigid_body_texture(env, actor_handle, 0, gymapi.MESH_VISUAL_AND_COLLISION, texture_handles[painted_texture_idx])
    

#########################
# Create multiple cameras
#########################

from camera import *

set_camera_pos(gym,env,args.DR_camera_pose,init_camera=True)

#########################
# Run simulation
#########################

if args.DR_obstacle_obj:
    ball_state = gym.get_actor_rigid_body_states(env, obj_handle["ball"], gymapi.STATE_POS)

frame_cnt = 0
seg_num_cnt = 0
rgb_num_cnt = 0
dep_num_cnt = 0
while not gym.query_viewer_has_closed(viewer):
    # get rope state
    frame_cnt += 1
    if args.Keyboard_control:
        for evt in gym.query_viewer_action_events(viewer):
            for i in range(0,6):
                if evt.action == first_body_event_namelist[i] and evt.value == 1.0:
                    first_body_control[i] = 1.0
                elif evt.action == first_body_event_namelist[i] and evt.value == 0.0:
                    first_body_control[i] = 0.0
                if evt.action == last_body_event_namelist[i] and evt.value == 1.0:
                    last_body_control[i] = 1.0
                elif evt.action == last_body_event_namelist[i] and evt.value == 0.0:
                    last_body_control[i] = 0.0
        for i in range(0,3):
            if first_body_control[i*2] == 1.0:
                first_body_tar_pos[i] += 0.01 
            elif first_body_control[i*2+1] == 1.0:
                first_body_tar_pos[i] -= 0.01 
            if last_body_control[i*2] == 1.0:
                last_body_tar_pos[i] += 0.01 
            elif last_body_control[i*2+1] == 1.0:
                last_body_tar_pos[i] -= 0.01 

    if frame_cnt % 25 == 0:

        #########################
        # Set object random positions
        #########################
        if args.dlo_seg_clean:    
            rand_pos = np.random.rand(3) * 2
            ball_state['pose']['p'].fill((rand_pos[0], rand_pos[1], rand_pos[2]))
            gym.set_actor_rigid_body_states(env, obj_handle["ball"], ball_state, gymapi.STATE_POS)

        #########################
        # Take images
        #########################
        for j in range(4):
            # The gym utility to write images to disk is recommended only for RGB images.
            rgb_filename = save_dir + "rgb_image/%d_80.png" % (rgb_num_cnt)
            gym.write_camera_image_to_file(sim, env, camera_handles[j], gymapi.IMAGE_COLOR, rgb_filename)
            rgb_num_cnt += 1
            # Depth image preprocessing 
            depth_image = gym.get_camera_image(sim, env, camera_handles[j], gymapi.IMAGE_DEPTH)
            depth_image[depth_image == -np.inf] = 0
            depth_image[depth_image < -10] = -10
            normalized_depth = -255.0*(depth_image/np.min(depth_image + 1e-4))
            normalized_depth_image = im.fromarray(normalized_depth.astype(np.uint8), mode="L")
            normalized_depth_image.save(save_dir + "dep_image/%d_80.png" % (dep_num_cnt))
            dep_num_cnt += 1

        #########################
        # Set all objects to a far place
        #########################
        if args.dlo_seg_clean:    
            prev_ball_state_x = ball_state['pose']['p'][0][0]
            prev_ball_state_y = ball_state['pose']['p'][0][1]
            prev_ball_state_z = ball_state['pose']['p'][0][2]

            ball_state['pose']['p'].fill((10, 10, 0))
            gym.set_actor_rigid_body_states(env, obj_handle["ball"], ball_state, gymapi.STATE_POS)
            gym.step_graphics(sim)
            gym.draw_viewer(viewer, sim, True)
            gym.render_all_camera_sensors(sim)
            gym.sync_frame_time(sim)

        #########################
        # Take segmentation images
        #########################  
        for j in range(4):
            # Segmentation image saving
            # seg_filename = save_dir + "seg_image/env%d_cam%d_frame%d_80.png" % (0, j, frame_cnt)
            seg_filename = save_dir + "seg_image/%d_80.png" % (seg_num_cnt)
            seg_image = gym.get_camera_image(sim, env, camera_handles[j], gymapi.IMAGE_SEGMENTATION)
            for i in range(len(seg_convert_dict)):
                seg_image[seg_image == i] = seg_convert_dict[i]
            seg_image = im.fromarray(seg_image.astype(np.uint8), mode="L")
            seg_image.save(seg_filename)
            seg_num_cnt += 1
        if args.dlo_seg_clean:    
            ball_state['pose']['p'].fill((prev_ball_state_x, prev_ball_state_y, prev_ball_state_z))
            gym.set_actor_rigid_body_states(env, obj_handle["ball"], ball_state, gymapi.STATE_POS)


    #########################
    # Set camera pose if DR_camera_pose
    #########################
    if frame_cnt % 120 == 0 and args.DR_camera_pose:
        set_camera_pos(gym,env,args.DR_camera_pose,init_camera=False)
    #########################
    # Attractor
    ######################### 

    body_state = gym.get_actor_rigid_body_states(env, obj_handle['rope'], gymapi.STATE_ALL)
    body_pos = body_state["pose"]["p"]
    body_ore = body_state["pose"]["r"]
    body_vel = body_state["vel"]["linear"]
    #print('body_pos', body_pos.shape)
    if frame_cnt % 60 == 0:
        if not args.Keyboard_control:
            last_body_tar_pos = np.random.rand(3,) * 1.7 - 0.3
            last_body_tar_pos[-1] += 0.2
            first_body_tar_pos = np.random.rand(3,) * 1.7 - 0.3
            first_body_tar_pos[-1] += 0.2
        if args.DR_dlo_color:
            rand_color = np.random.rand(3,)
            for i in range(0, last_body_idx+1):
                print(i,rand_color)
                set_color = gymapi.Vec3(rand_color[0],rand_color[1],rand_color[2])
                gym.set_rigid_body_color(env, obj_handle['rope'], i, gymapi.MESH_VISUAL_AND_COLLISION, set_color)
        if args.DR_lighting:
            set_DR_lighting(sim)
    forces, torques = apply_force(cur_pos=body_pos[last_body_idx],
                                  cur_ore=body_ore[last_body_idx],
                                  cur_vel=body_vel[last_body_idx],
                                  cur_ang=0,
                                  num_bodies=env_num_bodies,
                                  tar_pos=last_body_tar_pos,
                                  tar_ore=np.array([1.0, 0.0, 0.0]),
                                  body_index=last_body_idx)
    gym.apply_rigid_body_force_tensors(sim, gymtorch.unwrap_tensor(forces), gymtorch.unwrap_tensor(torques), gymapi.ENV_SPACE)
    
    forces, torques = apply_force(cur_pos=body_pos[first_body_idx],
                                  cur_ore=body_ore[first_body_idx],
                                  cur_vel=body_vel[first_body_idx],
                                  cur_ang=0,
                                  num_bodies=env_num_bodies,
                                  tar_pos=first_body_tar_pos,
                                  tar_ore=np.array([1.0, 0.0, 0.0]),
                                  body_index=first_body_idx)
    gym.apply_rigid_body_force_tensors(sim, gymtorch.unwrap_tensor(forces), gymtorch.unwrap_tensor(torques), gymapi.ENV_SPACE)
    
    #########################
    # Texture randomization
    #########################
    if frame_cnt % 10 == 0:
        if args.DR_texture:
            load_textures(env, asset_descriptors)

    #########################
    # Physical simulation
    #########################

    # step the physics
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    # update the viewer
    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)

    #########################
    # Camera rendering and images saving
    #########################
    gym.render_all_camera_sensors(sim)

    
    # Wait for dt to elapse in real time.
    # This synchronizes the physics simulation with the rendering rate.
    gym.sync_frame_time(sim)

print("Done")

gym.destroy_viewer(viewer)
gym.destroy_sim(sim)
