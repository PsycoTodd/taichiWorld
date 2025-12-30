# this is an extra try to test image pattern.
import taichi as ti
import taichi.math as tm
import numpy as np
from PIL import Image

ti.init(arch=ti.gpu)
w,h=320, 320

pixels = ti.Vector.field(3, dtype=ti.f64, shape=(w,h))
gui = ti.GUI("ImageNoise", res=(w,h))

def LoadImage(path: str):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    img = img.resize((w, h))
    img_array = np.array(img) / 255.0  # Normalize to [0, 1]

    return img_array


# Load image using PIL
baseImage = LoadImage('data/baseImage.webp')
noiseImage = LoadImage('data/008-perlin-noise.png')
maskImage = LoadImage('data/circle_mask.jpg')

@ti.kernel
def generate_image(baseImage: ti.types.ndarray(),
                   noiseImage: ti.types.ndarray(),
                   maskImage: ti.types.ndarray(),
                   time:float):
    for i, j in pixels:
        uv = tm.vec2(j/w, i/h)
        noiseUV = tm.fract(uv+time)
        noiseI, noiseJ = int(noiseUV.y * h), int(noiseUV.x * w)
        noise = noiseImage[noiseI, noiseJ, 0]
        noise = (2.0 * noise - 0.5) *0.02* maskImage[i, j, 0]
        baseI, baseJ = int(i + noise * h), int(j + noise * w)
        for k in ti.static(range(3)):
            pixels[i, j][k] = baseImage[baseJ, baseI, k]

i = 0
while gui.running:
    ex, ey = gui.get_cursor_pos()
    pixels.fill(0)
    generate_image(baseImage, noiseImage, maskImage, i*0.003)
    gui.set_image(pixels)
    gui.show()
    i += 1
