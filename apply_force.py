import math
import numpy as np
from numpy.lib.function_base import disp
from isaacgym import gymutil
from isaacgym import gymapi
from isaacgym import gymtorch
import torch


def apply_force(cur_pos,
                cur_ore,
                cur_vel,
                cur_ang,
                num_bodies,
                tar_pos=np.array([1.0,1.0,1.0]),
                tar_ore=np.array([1.0,0.0,0.0]),
                kp=16e-3,
                kd=10e-4,
                body_index=-1,
                device='cpu'):
    # env is set to 1
    tar_vel = np.array([0,0,0])
    tar_ang = np.array([0,0,0])
    forces = torch.zeros((1, num_bodies, 3), device=device, dtype=torch.float)
    torques = torch.zeros((1, num_bodies, 3), device=device, dtype=torch.float)
    for i in range(3):
        forces[0, body_index, i] = kp * (tar_pos[i] - cur_pos[i]) + kd * (tar_vel[i] - cur_vel[i])
        
        #torques[0, body_index, i] = kp * (tar_ore[i] - cur_ore[i]) - kd * tar_ang[i]
    return forces, torques
