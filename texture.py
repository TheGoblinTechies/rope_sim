import numpy as np
import os
from isaacgym import gymapi
from init import viewer, sim
from load_all import obj_handle

gym = gymapi.acquire_gym()

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
def load_textures(env, asset_descriptors):
    for i in range(len(asset_descriptors)):
        if asset_descriptors[i].asset_type != "core":
            actor_handle = obj_handle[asset_descriptors[i].asset_name]
            # DR_MODULAR_MARK
            painted_texture_idx = np.random.randint(len(texture_handles)-1,size=1)[0]
            gym.set_rigid_body_texture(env, actor_handle, 0, gymapi.MESH_VISUAL, texture_handles[painted_texture_idx])