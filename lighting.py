import numpy as np
from isaacgym import gymapi

def random_light():
    l_color = gymapi.Vec3(np.random.uniform(1, 1), np.random.uniform(1, 1), np.random.uniform(1, 1))
    l_ambient = gymapi.Vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1))
    l_direction = gymapi.Vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1))
    return l_color, l_ambient, l_direction