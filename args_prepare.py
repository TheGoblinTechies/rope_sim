#########################
# Processing argparse
#########################
from isaacgym import gymapi
import numpy as np
from init import viewer

#Example for how to use custom parameters
# args = gymutil.parse_arguments(
#     description="Domain Randomization Example",
#     headless=True,
#     custom_parameters=[
#         {"name": "--save_images", "action": "store_true", "help": "Store Images To Disk"}])


gym = gymapi.acquire_gym()

# # Domain randomization
import argparse
parser = argparse.ArgumentParser(description='Set parameters.')
parser.add_argument('--DR_all', type=bool, 
                                default=False,
                                help='decide if do domain randomization')
parser.add_argument('--DR_lighting', type=bool, 
                                     default=False, 
                                     help='random lighting conditions')
parser.add_argument('--DR_first_body', type=bool, 
                                       default=False, 
                                       help='random first body poses')
parser.add_argument('--DR_dlo_color', type=bool, 
                                      default=False, 
                                      help='random dlo color')
# parser.add_argument('--DR_texture_background', type=bool, 
#                                                default=False, 
#                                                help='random textures for background')
# parser.add_argument('--DR_texture_obstacle', type=bool, 
#                                              default=False, 
#                                              help='random textures for obstacle')
parser.add_argument('--DR_texture', type=bool, 
                                               default=False, 
                                               help='random textures')
parser.add_argument('--DR_robot_Franka', type=bool, 
                                           default=False, 
                                           help='random robot base positions and joint configurations')
parser.add_argument('--DR_robot_UR10', type=bool, 
                                           default=False, 
                                           help='random robot base positions and joint configurations')
parser.add_argument('--DR_obstacle_obj', type=bool, 
                                           default=False, 
                                           help='random object')

parser.add_argument('--DR_camera_pose', type=bool, 
                                        default=False, 
                                        help='random camera located positions and look-at positions')
parser.add_argument('--DR_obstacle_num', type=int, 
                                         default=1, 
                                         help='how many obstacles are used')
parser.add_argument('--dlo_seg_clean', type=bool, 
                                         default=False, 
                                         help='segmentation does not include occlusion parts')
# Control method
parser.add_argument('--Keyboard_control', type=bool,
                                          default=False,
                                          help='use keyboard to control two ends of the dlo')

args = parser.parse_args()

first_body_tar_pos = np.array([0.0, 0.0, 2.0])
last_body_tar_pos = np.array([1.0, 0.0, 2.0])

if args.Keyboard_control == True:
    first_body_control = []
    first_body_event_namelist = ["1_X+","1_X-","1_Y+","1_Y-","1_Z+","1_Z-"]
    first_body_event_keylist = [gymapi.KEY_W, gymapi.KEY_S,
                                gymapi.KEY_A, gymapi.KEY_D,
                                gymapi.KEY_Q, gymapi.KEY_E]
    for i in range(6):
        gym.subscribe_viewer_keyboard_event(viewer, first_body_event_keylist[i], first_body_event_namelist[i])
        first_body_control.append(0.0)

    last_body_control = []
    last_body_event_namelist = ["2_X+","2_X-","2_Y+","2_Y-","2_Z+","2_Z-"]
    last_body_event_keylist = [gymapi.KEY_I, gymapi.KEY_K,
                                gymapi.KEY_J, gymapi.KEY_L,
                                gymapi.KEY_U, gymapi.KEY_O]
    for i in range(6):
        gym.subscribe_viewer_keyboard_event(viewer, last_body_event_keylist[i], last_body_event_namelist[i])
        last_body_control.append(0.0)

    gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_SPACE, 'record_img')


def set_DR_lighting(sim):
    #########################
    # Set lighting conditions
    #########################
    if not args.DR_lighting:
        print("DR light is not enabled, please check your parser setting.")
        return
    
    # DR_MODULAR_MARK
    for i in range(0,1):
        l_color = gymapi.Vec3(np.random.uniform(1, 1), np.random.uniform(1, 1), np.random.uniform(1, 1))
        l_ambient = gymapi.Vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1))
        l_direction = gymapi.Vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1))

        #gym.set_light_parameters(sim, light_index, intensity, ambient, direction)
        gym.set_light_parameters(sim, i, l_color, l_ambient, l_direction)