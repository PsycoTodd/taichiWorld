# This is a tryout to enable distance field line with smooth fadeout and customizable thickness.
# a good interview concept in shader.

import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)
w,h=320, 320

pixels = ti.field(dtype=float, shape=(w,h))
gui = ti.GUI("2DLine", res=(w,h))

@ti.func
def distanceField(st: tm.vec2, startPt: tm.vec2, endPt: tm.vec2, w: float, h: float, thickness:float):
    st = st * 2 - 1
    bPt = startPt * 2 - 1
    ePt = endPt * 2 - 1
    k = tm.dot(st - bPt, ePt - bPt) / tm.dot(ePt - bPt, ePt - bPt)
    dV = (st - bPt) - tm.clamp(k, 0.0, 1.0) * (ePt - bPt)
    dist = tm.length(dV * tm.vec2(w, h))
    return 1.0 - tm.smoothstep(0.0, thickness, dist)
@ti.kernel
def paint(ex: float, ey: float, t: float):
    for x, y in pixels:
        sy = y/h
        sx = x/w
        color = distanceField(tm.vec2(sx, sy), 
                              tm.vec2(0.5, 0.5), 
                              tm.vec2(ex, ey), w, h, 5)
        pixels[x,y] = color

i = 0
while gui.running:
    ex, ey = gui.get_cursor_pos()
    pixels.fill(0)
    paint(ex, ey, i)
    gui.set_image(pixels)
    gui.show()
    i += 1