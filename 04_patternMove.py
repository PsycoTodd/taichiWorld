# https://thebookofshaders.com/09/

import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)
w,h = 320, 320

pixels = ti.field(dtype=float, shape=(w,h))
gui = ti.GUI("PatternMove", res=(w,h))

@ti.func
def circle(st: tm.vec2, size: float)->float:
    st = 0.5 - st
    return tm.step(0.25 * size * size, tm.dot(st,st))

@ti.func
def rotate2d(angle: float)->tm.mat2:
    return tm.mat2(tm.cos(angle), -tm.sin(angle),
                   tm.sin(angle), tm.cos(angle))

@ti.func
def moveTiles(st:tm.vec2, partNum: float, time: float, changeGap: float)->tm.vec2:
    st *= partNum
    
    if (tm.mod(time/changeGap, 2.0)>1):
        st.y += (0.5-tm.step(1, tm.mod(st.x, 2.0))) * time
    else:
        st.x += (0.5-tm.step(1, tm.mod(st.y, 2.0))) * time
    st = tm.fract(st)
    return st


@ti.kernel
def paint(t: float):
    speed = 0.8
    for x, y in pixels:
        sy = y/h
        sx = x/w
        st = tm.vec2(sx, sy)
        st = moveTiles(st, 10, t, 5)
        pixels[x,y] = circle(st, 0.5)

i = 0
while gui.running:
    pixels.fill(0)
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1