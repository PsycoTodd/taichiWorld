# https://thebookofshaders.com/06/

import taichi as ti
import taichi.math as tm


ti.init(arch=ti.gpu)

n = 320
pixels = ti.Vector.field(3, dtype=float, shape=(n, n))


gui = ti.GUI("HSB", res = (n, n))

@ti.func
def hsb2rgb(c: tm.vec3)-> tm.vec3:
    rgb = tm.clamp(abs(tm.mod(c.x * 6.0 + tm.vec3(0.0, 4.0, 2.0), 6.0)-3.0)-1.0, 0.0, 1.0)
    rgb = rgb * rgb * (3.0 - 2.0 * rgb)
    return c.z * tm.mix(tm.vec3(1.0), rgb, c.y)

@ti.kernel
def paint(t: float):
    for x, y in pixels:
        sy = y/n
        sx = x/n
        color = hsb2rgb(tm.vec3(sx, 1.0, sy))
        pixels[x, y] = color 

i=0
while gui.running:
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1