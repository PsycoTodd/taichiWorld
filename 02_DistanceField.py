#https://thebookofshaders.com/08/

import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)
w,h=320,320

pixels = ti.field(dtype=float, shape=(w, h))

gui = ti.GUI("DistanceField", res = (w, h))

@ti.func
def distanceField(st: tm.vec2, center: tm.vec2)->float:
    st = st * 2 - 1
    d = tm.length(abs(st)-center)
    return tm.fract(d*10)

@ti.kernel
def paint(t: float):
    speed = 0.2
    for x, y in pixels:
        sy = y/h
        sx = x/w
        color = distanceField(tm.vec2(sx, sy), tm.vec2(abs(tm.sin(t*speed))))
        pixels[x,y] = color


i = 0
while gui.running:
    paint(i*0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1