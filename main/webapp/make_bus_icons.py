from PIL import Image
import numpy as np

orig_img = np.array(Image.open('bus.png'))
colors = [
    [0,0,0],
    [255,0,0],
    [0,255,0],
    [0,0,255],
    [255,255,0],
    [0,255,255],
    [255,0,255],
    [255,255,255]
]

for i, color in enumerate(colors):
    img = orig_img.copy()
    img[:,:,0] = color[0]
    img[:,:,1] = color[1]
    img[:,:,2] = color[2]
    pil_img = Image.fromarray(img)
    pil_img.save('%d.png'%i)