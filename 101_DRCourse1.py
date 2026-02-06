import taichi as ti
import taichi.math as tm

ti.init(arch=ti.gpu)

triangle = ti.Vector.field(dtype=ti.f32, n=2, shape=(3), needs_grad=True)
triangle[0] = tm.vec2(110.1, 110.2) # a
triangle[1] = tm.vec2(190.3, 110.4) # b
triangle[2] = tm.vec2(150.5, 150.6) # c

loss = ti.field(dtype=ti.f32, shape=(), needs_grad=True)
loss.grad[None] = 1.0
w,h=320,320

image = ti.field(dtype=ti.f32, shape=(w, h), needs_grad=True)

gui = ti.GUI("NoiseSphere", res = (w, h))

@ti.func
def is_pixel_in_triangle(pixel: tm.vec2) -> bool:
    ab = triangle[1] - triangle[0]
    ac = triangle[2] - triangle[0]
    bc = triangle[2] - triangle[1]
    ap = pixel - triangle[0]
    bp = pixel - triangle[1]
    cp = pixel - triangle[2]
    area_abc = abs(tm.cross(ab, ac))
    area_abp = abs(tm.cross(ap, ab))
    area_acp = abs(tm.cross(ap, ac))
    area_bcp = abs(tm.cross(bp, bc))
    u = area_abp / area_abc
    v = area_acp / area_abc
    w = area_bcp / area_abc
    return (u<0 or u>1) or (v<0 or v>1) or (w<0 or w>1)


@ti.kernel
def render():
    for pixel in ti.grouped(image):
        if is_pixel_in_triangle(pixel):
            image[*pixel] = 1.0
        else:
            image[*pixel] = 0.0

@ti.kernel
def compute_loss():
    for pixel in ti.grouped(image):
        loss[None] += image[*pixel]

while gui.running:
    loss.fill(0.0)
    triangle[2].y += 1e-2
    render()
    compute_loss()
    gui.set_image(image)
    print("Loss =", loss[None])
    gui.show()