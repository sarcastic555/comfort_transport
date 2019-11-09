from PIL import Image
import numpy as np

def draw_contour(img):
    d = 5
    h = img.shape[0]
    w = img.shape[1]
    contour = np.full((img.shape[0],img.shape[1]), 0)
    for y in range(d, h-d):
        for x in range(d, w-d):
            if img[y-d][x-d][3] > 125 or img[y-d][x+d][3] > 125 or img[y+d][x-d][3] > 125 or img[y+d][x+d][3] > 125:
                if img[y][x][3] < 125:
                    contour[y][x] = 1
    for y in range(h):
        for x in range(w):
            if contour[y,x] == 1:
                img[y][x][0] = 255
                img[y][x][1] = 255
                img[y][x][2] = 255
                img[y][x][3] = 255
    return img

def pad_front_window(img):
    left = 100
    right = 480 - 100
    top = 100
    bottom = 270
    for y in range(top, bottom):
        for x in range(left, right):
            img[y][x][3] = 255
    return img


orig_img = np.array(Image.open('bus.png'))
colors = [
    [0,0,0],
    [255,0,0],
    [0,255,0],
    [0,0,255],
    [255,255,0],
    [0,255,255],
    [255,0,255],
]


for i, color in enumerate(colors):
    img = orig_img.copy()
    img[:,:,0] = color[0]
    img[:,:,1] = color[1]
    img[:,:,2] = color[2]
    img = pad_front_window(img)
    img = draw_contour(img)
    pil_img = Image.fromarray(img)
    pil_img.save('%d.png'%i)
    
