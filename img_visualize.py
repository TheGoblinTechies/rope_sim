import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import numpy as np
np.set_printoptions(threshold=np.inf)
import cv2
import matplotlib.pyplot as plt
def visualize(**images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
    plt.show()

mask = cv2.imread('../camera_data/seg_image_clean/0.png')
print(np.max(mask))
print(mask.shape)
visualize(mask=mask)
