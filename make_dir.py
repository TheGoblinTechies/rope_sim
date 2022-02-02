import os

if not os.path.exists("../camera_data"):
    os.mkdir("../camera_data")

if not os.path.exists("../camera_data/seg_image"):
    os.mkdir("../camera_data/seg_image")

if not os.path.exists("../camera_data/rgb_image"):
    os.mkdir("../camera_data/rgb_image")

if not os.path.exists("../camera_data/dep_image"):
    os.mkdir("../camera_data/dep_image")

if not os.path.exists("../camera_data/test_data"):
    os.mkdir("../camera_data/test_data")

if not os.path.exists("../camera_data/test_data/seg_image"):
    os.mkdir("../camera_data/test_data/seg_image")

if not os.path.exists("../camera_data/test_data/rgb_image"):
    os.mkdir("../camera_data/test_data/rgb_image")

if not os.path.exists("../camera_data/test_data/dep_image"):
    os.mkdir("../camera_data/test_data/dep_image")
