
#########################
# Attractor handles creation
#########################

# attractor_handles = [] 
# for i in range(len(asset_descriptors)):
#     if asset_descriptors[i].asset_type == "core":
#         # set attractor properties for rope
#         rope_handle = obj_handle[obj_namelist[i]]
#         body_dict = gym.get_actor_rigid_body_dict(env, rope_handle)
#         props = gym.get_actor_rigid_body_states(env, rope_handle, gymapi.STATE_POS)
#         # print(props)
#         rope_first_body_pose = props['pose'][:][body_dict[asset_descriptors[i].asset_first_body]]
#         rope_last_body_pose = props['pose'][:][body_dict[asset_descriptors[i].asset_last_body]]
        
#         rope_first_body_handle = gym.find_actor_rigid_body_handle(env, rope_handle, asset_descriptors[i].asset_first_body)
#         rope_last_body_handle = gym.find_actor_rigid_body_handle(env, rope_handle, asset_descriptors[i].asset_last_body)

#         # set up first body
#         first_body_attractor_properties = last_body_attractor_properties = gymapi.AttractorProperties()
#         first_body_attractor_properties.stiffness = last_body_attractor_properties.stiffness = 1e3
#         first_body_attractor_properties.damping = last_body_attractor_properties.damping = 1e3
#         first_body_attractor_properties.axes = last_body_attractor_properties.axes = gymapi.AXIS_ALL
        
#         first_body_attractor_properties.target = rope_first_body_pose
#         last_body_attractor_properties.target = rope_last_body_pose
        
#         # print('rope_first_body',rope_first_body_pose)
#         # print('rope_last_body',rope_last_body_pose)

#         # pose = gymapi.Transform()
#         # pose.p = gymapi.Vec3(0, 0.0, 0.0)
#         # pose.r = gymapi.Quat(-0.707107, 0.0, 0.0, 0.707107)
#         first_body_attractor_handle = gym.create_rigid_body_attractor(env, first_body_attractor_properties)
#         last_body_attractor_handle = gym.create_rigid_body_attractor(env, last_body_attractor_properties)
#         attractor_handles.append(first_body_attractor_handle)
#         attractor_handles.append(last_body_attractor_handle)    # elif asset_descriptors[i].asset_type == "obstacle" and "robot" in asset_descriptors[i].asset_type:
#     #     # control robot arm
#     #     attractor_properties = gymapi.AttractorProperties()
#     #     attractor_properties.stiffness = 1e2
#     #     attractor_properties.damping = 1e2
#     #     attractor_properties.axes = gymapi.AXIS_ALL

# def update_rope():
#     for i in [0, 1]:
#         attractor_properties = gym.get_attractor_properties(env, attractor_handles[i])
#         pose = attractor_properties.target
#         pose.p.x = pose.p.x + (np.random.rand(1)[0])*100
#         pose.p.y = pose.p.y + (np.random.rand(1)[0])*100
#         pose.p.z = pose.p.z + (np.random.rand(1)[0])*100
#         print("Set to new position --- ", i, "-body to", pose.p)
#         gym.set_attractor_target(env, attractor_handles[i], pose)
