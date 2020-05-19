import vpython as v
import numpy as np

data = np.load("../data/D_WT_1000SS.p", allow_pickle=True)
exp_number = 0
posx = data[exp_number]["x"]
posy = data[exp_number]["y"]
init_pos = v.vector(0, 0, 10)
s = v.sphere(pos=init_pos, color=v.color.magenta, radius=2.5)
spring = v.helix(pos=v.vector(0, 0, 0), color=v.color.green, axis=s.pos, coils=5, thickness=0.1, constant=1)

for i in range(len(posx)):

    v.rate(100)
    s.pos = v.vector(posx[i], posy[i], 0) + init_pos
    spring.axis = s.pos
    print(spring.pos)