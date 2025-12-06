import taichi as ti
import taichi.math as tm


ti.init(arch=ti.gpu)

n = 320
pixels = ti.Vector.field(3, dtype=float, shape=(n, n))


@ti.kernel
def paint(t: float):
    red = [1, 0, 0]
    green = [0, 1, 0]
    for y, x in pixels:
        p1 = y/n
        p2 = x/n
        p = tm.sqrt(p1*p1+p2*p2) / tm.sqrt(2) * (1+tm.sin(t))/2
        for k in ti.static(range(3)):
            pixels[y, x][k] = tm.mix(red[k], green[k], p)

gui = ti.GUI("Hello world", res = (n, n))

i=0
while gui.running:
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
    i += 1