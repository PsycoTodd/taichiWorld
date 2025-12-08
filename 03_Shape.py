#https://thebookofshaders.com/08/

import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)
w,h = 320, 320

pixels = ti.field(dtype=float, shape=(w,h))
gui = ti.GUI("Transform", res=(w,h))

@ti.func
def box(st: tm.vec2, size: tm.vec2)->float:
    size = 0.5 - size*0.5
    uv = tm.smoothstep(size, size+0.001, st)
    uv *= tm.smoothstep(size, size+0.001, 1.0-st)
    return uv.x * uv.y

@ti.func
def cross(st: tm.vec2, size: float)->float:
    return box(st, tm.vec2(size, size/4.)) + box(st, tm.vec2(size/4, size))

@ti.func
def rotate2d(angle: float)->tm.mat2:
    return tm.mat2(tm.cos(angle), -tm.sin(angle),
                   tm.sin(angle), tm.cos(angle))

@ti.kernel
def paint(t: float):
    speed = 0.8
    for x, y in pixels:
        sy = y/h
        sx = x/w
        st = tm.vec2(sx, sy)
        st -= 0.5
        st = rotate2d(tm.sin(t*speed)*tm.pi) @ st
        st += 0.5
        pixels[x,y] += cross(st, 0.4)

i = 0
while gui.running:
    pixels.fill(0)
    paint(i*0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1