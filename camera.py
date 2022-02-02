import math
import numpy as np
from init import spacing
from isaacgym import gymutil
from isaacgym import gymapi
from isaacgym import gymtorch


# Create 4 cameras in each environment
# From four corners

camera_handles = []

# DR_MODULAR_MARK
camera_properties = gymapi.CameraProperties()
camera_properties.horizontal_fov = 72.0
camera_properties.width = 1280
camera_properties.height = 720

# camera position and look-to position
# for DR
camera_pos_z_unit = 3
camera_pos_x_unit = 1.5
camera_pos_y_unit = 1.5
camera_lookat_x_unit = 1
camera_lookat_y_unit = 1

camera_pos_x_dir = [-1, -1, 1, 1]
camera_pos_y_dir = [-1, 1, -1, 1]

seg_convert_dict = [60, 120, 180, 240]

def set_camera_pos(gym, env, DR_camera, init_camera):
    for i in range(0,4):
        # Set a fixed position and look-target for the first camera
        # position and target location are in the coordinate frame of the environment
        if init_camera:
            camera = gym.create_camera_sensor(env, camera_properties)
        camera_position_DR = (np.random.rand(6,)-0.5) * 0.1
        if not DR_camera:
            camera_position_DR *= 0
        camera_position = gymapi.Vec3(camera_pos_x_unit * camera_pos_x_dir[i] + camera_position_DR[0],
                                      camera_pos_y_unit * camera_pos_y_dir[i] + camera_position_DR[1],
                                      camera_pos_z_unit + camera_position_DR[2])
        camera_target = gymapi.Vec3((camera_lookat_x_unit * -camera_pos_x_dir[i] + camera_position_DR[3])*0.5,
                                    (camera_lookat_y_unit * -camera_pos_y_dir[i] + camera_position_DR[4])*0.5,
                                    camera_pos_z_unit*0 + camera_position_DR[5])
        if init_camera:
            gym.set_camera_location(camera, env, camera_position, camera_target)
            camera_handles.append(camera)
        else:
            gym.set_camera_location(camera_handles[i], env, camera_position, camera_target)

