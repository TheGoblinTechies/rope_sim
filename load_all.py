import numpy as np
from isaacgym import gymapi
from init import viewer, sim

gym = gymapi.acquire_gym()

# to load objs
class AssetDesc:
    def __init__(self, file_name,
                 flip_visual_attachments=False,
                 mesh_normal_mode=gymapi.FROM_ASSET,
                 asset_type="core",
                 asset_name="rope",
                 lastbody_name="B80",
                 asset_scaling=1.0,
                 asset_fixed = True,
                 asset_position=np.array([0.0, 0.0, 1.0]),
                 asset_orientation=np.array([-0.707107, 0.0, 0.0, 0.707107])):
        
        self.file_name = file_name
        self.flip_visual_attachments = flip_visual_attachments
        self.mesh_normal_mode = mesh_normal_mode
        # type: core, room, obstacle
        self.asset_type=asset_type
        # name: rope, wall & ground, ball, cube, robot
        self.asset_name=asset_name
        # scaling: set scaling factor for object as DR
        self.asset_scaling=asset_scaling
        # fixed: if fixed base
        self.asset_fixed = asset_fixed
        # transform
        pose = gymapi.Transform()
        pose.p = gymapi.Vec3(asset_position[0], asset_position[1], asset_position[2])
        pose.r = gymapi.Quat(asset_orientation[0], asset_orientation[1], asset_orientation[2], asset_orientation[3])
        self.asset_pose = pose
        if self.asset_type == "core":
            self.asset_first_body_name = "B0"
            self.asset_last_body_name = lastbody_name
        
wall_position = 3
asset_descriptors = [
    #AssetDesc("mjcf/rope/rope_stiff.xml", False, gymapi.COMPUTE_PER_VERTEX, asset_type="core", asset_fixed = False, asset_name="rope",asset_scaling=1.2, asset_position=[0,0,2]),
    AssetDesc("mjcf/rope/rope_80.xml", False, gymapi.COMPUTE_PER_VERTEX, asset_type="core", asset_fixed = False, asset_name="rope", lastbody_name="B80", asset_scaling=1.2, asset_position=[0,0,2.0]),
    AssetDesc("mjcf/rope/rope_60.xml", False, gymapi.COMPUTE_PER_VERTEX, asset_type="core", asset_fixed = False, asset_name="rope", lastbody_name="B60", asset_scaling=1.2, asset_position=[0,0,1.8]),
    AssetDesc("mjcf/rope/rope_40.xml", False, gymapi.COMPUTE_PER_VERTEX, asset_type="core", asset_fixed = False, asset_name="rope", lastbody_name="B40", asset_scaling=1.2, asset_position=[0,0,1.6]),
    # to-do
    # import walls
    # see https://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/steps/index.htm
    # AssetDesc("urdf/wall_as_ball.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="room", asset_name="wall_nx_0", asset_position=[-wall_position,0,0], asset_orientation=[0.707,0.707,0,0]),
    # AssetDesc("urdf/wall_as_ball.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="room", asset_name="wall_0_y", asset_position=[0,wall_position,0], asset_orientation=[1,0,0,0]),
    # AssetDesc("urdf/wall_as_ball.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="room", asset_name="wall_x_0", asset_position=[wall_position,0,0], asset_orientation=[0.707,0.707,0,0]),
    # AssetDesc("urdf/wall_as_ball.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="room", asset_name="wall_0_ny", asset_position=[0,-wall_position,0], asset_orientation=[1,0,0,0]),
    # # import ground
    # AssetDesc("urdf/wall.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="room", asset_name="ground", asset_position=[0,0,0]),
    # # import other objects
    # AssetDesc("urdf/ball.urdf", False, gymapi.COMPUTE_PER_VERTEX, asset_type="obstacle", asset_name="ball"),
]

obj_typeDict = {i.asset_name: i.asset_type for i in asset_descriptors}
obj_namelist = [i.asset_name for i in asset_descriptors]
obj_indexDict = {asset_descriptors[i].asset_name: i for i in range(len(asset_descriptors))}
obj_scalingDict = {i.asset_name: i.asset_scaling for i in asset_descriptors}
obj_fixedDict = {i.asset_name: i.asset_fixed for i in asset_descriptors}

print(obj_typeDict)
print(obj_namelist)
print(obj_indexDict)
print(obj_scalingDict)
print(obj_fixedDict)


# load asset
asset_root = "../../assets"

assets = []
for asset_desc in asset_descriptors:
    asset_file = asset_desc.file_name
    asset_options = gymapi.AssetOptions()
    asset_options.fix_base_link = asset_desc.asset_fixed
    asset_options.flip_visual_attachments = asset_desc.flip_visual_attachments
    asset_options.use_mesh_materials = False
    asset_options.mesh_normal_mode = asset_desc.mesh_normal_mode

    print("No.%d: Loading asset '%s' from '%s'" % (obj_indexDict[asset_desc.asset_name], asset_file, asset_root))
    assets.append(gym.load_asset(sim, asset_root, asset_file, asset_options))

# for apply force
# sim_params.use_gpu_pipeline = args.use_gpu_pipeline
device = 'cpu'
env_num_bodies = 0
for i in range(len(asset_descriptors)):
    env_num_bodies += gym.get_asset_rigid_body_count(assets[i])


#########################
# Setup world and viewer
#########################

# set up the env grid
num_per_row = 1
spacing = 6
env_lower = gymapi.Vec3(-spacing, -spacing, 0.0)
env_upper = gymapi.Vec3(spacing, spacing, spacing)

# position the camera
# cam_pos = gymapi.Vec3(17.2, 2.0, 16)
# cam_target = gymapi.Vec3(5, -2.5, 13)
cam_pos = gymapi.Vec3(7.2, 2.0, 6)
cam_target = gymapi.Vec3(0, -2.5, 0)



gym.viewer_camera_look_at(viewer, None, cam_pos, cam_target)

# cache useful handles
# create env
# only one env
env = gym.create_env(sim, env_lower, env_upper, num_per_row)

# Here a trick to set segmentationId is:
# set rope to 1,2,...
# set all other object to 0 as well as walls and the ground
obj_handle = {}

for i in range(len(asset_descriptors)):
    obj_handle[obj_namelist[i]] = gym.create_actor(env, assets[i],
                                                   asset_descriptors[i].asset_pose,
                                                   asset_descriptors[i].asset_name,
                                                   group=0,
                                                   filter=0,
                                                   segmentationId=1 if asset_descriptors[i].asset_type=="core" else 0)
    gym.set_actor_scale(env, obj_handle[obj_namelist[i]], asset_descriptors[i].asset_scaling)

