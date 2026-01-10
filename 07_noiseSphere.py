# https://thebookofshaders.com/11/ first part on 1d noise.

import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)
w,h=320,320

pixels = ti.field(dtype=float, shape=(w, h))

gui = ti.GUI("NoiseSphere", res = (w, h))

@ti.func
def sphere(st: tm.vec2, center: tm.vec2, radius:float, factor:float)->float:
    st = st * 2 - 1
    a = tm.atan2(st.y,st.x)
    m = abs(tm.mod(a+factor*2.,3.14*2.)-3.14)/3.6 + noise(st + factor*0.1)*0.5
    d = tm.length(abs(st)-center)
    d += tm.sin(a*20.) * 0.1 * pow(m, 2.2) +  tm.sin(a*50.)*noise(st+factor*.2)*.1
    return 1.0 - tm.step(d, radius) * (1.0 - tm.step(d, radius * 0.95))

@ti.func
def selfRand(i: float)->float:
    return tm.fract(tm.sin(i)*30000.0)

@ti.func
def noise(st: tm.vec2)->float:
    i = tm.floor(st)
    f = tm.fract(st)

    u = f*f*(3.0-2.0*f)

    return tm.mix( tm.mix( tm.dot( selfRand(i + tm.vec2(0.0,0.0) ), f - tm.vec2(0.0,0.0) ),
                     tm.dot( selfRand(i + tm.vec2(1.0,0.0) ), f - tm.vec2(1.0,0.0) ), u.x),
                tm.mix( tm.dot( selfRand(i + tm.vec2(0.0,1.0) ), f - tm.vec2(0.0,1.0) ),
                     tm.dot( selfRand(i + tm.vec2(1.0,1.0) ), f - tm.vec2(1.0,1.0) ), u.x), u.y)

@ti.func
# this won't work, 2D still need 2D to float noise
def OneDnoise(v: float)->float:
    i = tm.floor(v)
    f = tm.fract(v)
    y = selfRand(i)
    y = tm.mix(selfRand(i), selfRand(i+1.0), f)
    return y

@ti.kernel
def paint(t: float):
    for x, y in pixels:
        sy = y/h
        sx = x/w
        color = sphere(tm.vec2(sx, sy), tm.vec2(0, 0), 0.5, t)
        pixels[x,y] = color


i = 0
while gui.running:
    paint(i*0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1