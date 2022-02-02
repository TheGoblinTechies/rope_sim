from isaacgym import gymutil
from isaacgym import gymapi
# args_isaacgym = gymutil.parse_arguments()
# print(args_isaacgym)
# initialize gym
gym = gymapi.acquire_gym()

# configure sim
sim_params = gymapi.SimParams()
sim_params.dt = dt = 1.0 / 60.0
sim_params.physx.solver_type = 1
sim_params.physx.num_position_iterations = 6
sim_params.physx.num_velocity_iterations = 0
sim_params.physx.num_threads = 0
sim_params.physx.use_gpu = True
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)

sim_params.use_gpu_pipeline = False

sim = gym.create_sim(0, 0, gymapi.SIM_PHYSX, sim_params)

# add ground plane
plane_params = gymapi.PlaneParams()
plane_params.normal = gymapi.Vec3(0, 0, 1)
gym.add_ground(sim, plane_params)

# add dlo param
first_body_idx = 0
last_body_idx = 80

# set spacing
spacing = 2.0


# saved image dir
# save_dir = '../camera_data/test_data/'
save_dir = '../camera_data/'

# create viewer
viewer = gym.create_viewer(sim, gymapi.CameraProperties())
if viewer is None:
    print("*** Failed to create viewer")
    quit()

# from isaacgym import gymutil
# from isaacgym import gymapi
# args = gymutil.parse_arguments()

# # initialize gym
# gym = gymapi.acquire_gym()

# # configure sim
# sim_params = gymapi.SimParams()
# sim_params.dt = dt = 1.0 / 60.0
# if args.physics_engine == gymapi.SIM_FLEX:
#     pass
# elif args.physics_engine == gymapi.SIM_PHYSX:
#     sim_params.physx.solver_type = 1
#     sim_params.physx.num_position_iterations = 6
#     sim_params.physx.num_velocity_iterations = 0
#     sim_params.physx.num_threads = args.num_threads
#     sim_params.physx.use_gpu = args.use_gpu
#     sim_params.up_axis = gymapi.UP_AXIS_Z
#     sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)

# sim_params.use_gpu_pipeline = False
# if args.use_gpu_pipeline:
#     print("WARNING: Forcing CPU pipeline.")

# sim = gym.create_sim(args.compute_device_id, args.graphics_device_id, args.physics_engine, sim_params)

# # add ground plane
# plane_params = gymapi.PlaneParams()
# plane_params.normal = gymapi.Vec3(0, 0, 1)
# gym.add_ground(sim, plane_params)

# # create viewer
# viewer = gym.create_viewer(sim, gymapi.CameraProperties())
# if viewer is None:
#     print("*** Failed to create viewer")
#     quit()
