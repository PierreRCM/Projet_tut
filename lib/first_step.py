import vpython as v
import numpy as np
import sys
import math as m
sys.path.insert(1, "/home/martin/Desktop/Intership_project/lib")
import simulated_motor_lib as sim
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def check_in_stator(position, list_stator_pos, stator_radius, dr):

    in_stator = False
    position += dr
    for stator in list_stator_pos:

        stator_pos = stator.pos
        pos_ref = stator_pos - position
        norm_pos_xy = m.sqrt(pos_ref.x**2 + pos_ref.y**2)

        if norm_pos_xy < stator_radius and position.z >= 0:

            in_stator = True
            # Faire avancer la boule dans le stator ? La supprimer et faire le crochet ?
    return in_stator


def check_border(border, sphere, dr):

    outbound = False
    if not (border[0][0] < sphere.pos.x + dr.x < border[0][1]):

        outbound = True

    elif not (border[1][0] < sphere.pos.y + dr.y < border[1][1]):

        outbound = True

    elif not (border[2][0] > sphere.pos.z + dr.z > border[2][1]):
        outbound = True

    return outbound


def model(t, P):

    return 1000*np.exp(-P*t)


# motor_angle, bead_angle = sim.SimulateTrace(bead_radius=500e-9, axis_offset=200e-9, speed_hz=55, numsteps=400, trace_length_s=5, Nstates=1, FPS=10000, k_hook= 400*1e-9*1e-12)

# data = np.load("../data/D_WT_1000SS.p", allow_pickle=True)
Kb = 1.38e-23
T = 295.
eta = 0.954e-3  # Viscosité de l'eau
rayon_part = 200E-12
D = Kb*T/(6*np.pi*eta*rayon_part)
wall_width = 0.01
# object pos
init_pos = v.vector(0, 0, 0)
sphere_pos = v.vector(0, 0, 5)
helix_pos = v.vector(0, 0, 0)
box_back = v.vector(0, 0, -10)
box_bottom = v.vector(0, -5, -5)
box_top = v.vector(0, 5, -5)
box_left = v.vector(-5, 0, -5)
box_right = v.vector(5, 0, -5)
s = v.sphere(pos=sphere_pos, color=v.color.magenta, radius=2.5)
spring = v.helix(pos=helix_pos, color=v.color.green, axis=s.pos, coils=5, thickness=0.1, constant=1)
# x = v.arrow(pos=init_pos + v.vector(5, 5, 0), axis=v.vector(10, 0, 0), color=v.color.blue)
# y = v.arrow(pos=init_pos+ v.vector(5, 5, 0), axis=v.vector(0, 10, 0), color=v.color.green)
# z = v.arrow(pos=init_pos+ v.vector(5, 5, 0), axis=v.vector(0, 0, 10), color=v.color.red)

# my_box_left = v.box(pos=box_left, length=wall_width, height=10, width=10, color=v.color.yellow, opacity=0.5)
# my_box_right = v.box(pos=box_right, length=wall_width, height=10, width=10, color=v.color.yellow, opacity=0.5)
# my_box_front = v.box(pos=init_pos, length=10, height=10, width=wall_width, color=v.color.yellow, opacity=0.5)
# my_box_back = v.box(pos=box_back, length=10, height=10, width=wall_width, color=v.color.yellow, opacity=0.5)
# my_box_bottom = v.box(pos=box_bottom, length=10, height=wall_width, width=10, color=v.color.yellow, opacity=0.5)
# my_box_top = v.box(pos=box_top, length=10, height=wall_width, width=10, color=v.color.yellow, opacity=0.5)
stator_number = 8
stator_r = 0.1  # 1 = 10 nm
stator_thickness = 0.03
# 1er biais : Mauvaise valeur de D possible
# turn_per_nanosec = 1/dt
dt = 1/30  # correspond au petit tho

step_size = 0.02  # rad
angle = 0
sphere_state = []
time_list = []
max_stator = 8

tot_sphere = 1
list_stator_pos = [
    v.ring(pos=v.vector(0.8*m.cos(2 * np.pi * x / max_stator), 0.8*m.sin(2 * np.pi * x / max_stator), 0),
           axis=v.vector(0, 0, 1), radius=stator_r, thickness=stator_thickness, color=v.color.green) for x in
    range(max_stator)]

coef_red_vol = 1

height = 9 # 1 = 10 nm
width = 9
length = 9

tot_time = 0
a = 0.0475
turn = 0.0
D_th = a**2/dt  # = 1.13*10^-2 (10nm)²/ns
tour_de_boucle = 0
nb_step = 0
# h_cube = (height/a)
# l_cube = (length/a)
# w_cube = (width/a)
bounds = [[-height/(2*coef_red_vol), height/(2*coef_red_vol)], [-length/(2*coef_red_vol), length/(2*coef_red_vol)],
          [width/coef_red_vol, 0]]
list_sphere = [v.sphere(pos=v.vector(np.random.uniform(bounds[0][0], bounds[0][1]),
                                     np.random.uniform(bounds[1][0], bounds[1][1]),
                                     np.random.uniform(bounds[2][0], bounds[2][1])),
                        color=v.color.red, radius=0.03) for x in range(tot_sphere)]

# nb_case_possible = h_cube*l_cube*w_cube
# dimension = 3
# surface_stator = stator_number * ((stator_r/10)**2 *np.pi)
# surf_cube = a**2
# surf_stator_cube = surface_stator/surf_cube  # nombre de cube correspondant a la surface total des stators
# proba_in_stator = (1/(2*dimension))*(surf_stator_cube/nb_case_possible)  # proba pour une bille de passer dans un stator
N_dt = []
list_dt = []

while tot_time < 1500000:
    #
    v.rate(1000000)

    for sphere in list_sphere:

        choose_dir = random.choice(["x", "y", "z"])
        if choose_dir == "x":
            x = random.choice([-a, a])
            dr = v.vector(x, 0, 0)

        elif choose_dir == "y":
            y = random.choice([-a, a])
            dr = v.vector(0, y, 0)

        else:
            z = random.choice([-a, a])
            dr = v.vector(0, 0, z)

        if not check_border(bounds, sphere, dr):
            sphere.pos += dr

        elif check_in_stator(sphere.pos, list_stator_pos, stator_r, dr):

            sphere.visible = False
            list_sphere.remove(sphere)
            del sphere
            angle += step_size
            posx = m.cos(angle)
            posy = m.sin(angle)
            s.pos = v.vector(posx, posy, 0) + sphere_pos
            spring.axis = s.pos
            new_sphere = v.sphere(pos=v.vector(np.random.uniform(bounds[0][0], bounds[0][1]),
                                     np.random.uniform(bounds[1][0], bounds[1][1]),
                                     np.random.uniform(bounds[2][0], bounds[2][1])), color=v.color.red, radius=0.03)

            list_sphere.append(new_sphere)
            nb_step += 1
            # print(nb_step/(tour_de_boucle*tot_sphere))

    # N_dt.append(len(list_sphere))
    # list_dt.append(tot_time)
    tot_time += dt
    tour_de_boucle += 1
    # sphere_state.append(len(list_sphere))
    # time_list.append(tot_time)
print(nb_step)
# para, pcov = curve_fit(model, list_dt, N_dt)
# plt.plot(list_dt, N_dt, label="Simulation")
# plt.plot(list_dt, model(np.array(list_dt), para[0]), label="Modèle P_exit = {:.5f}".format(para[0]))
# plt.ylabel("Number of particle")
# plt.xlabel("time (nanoseconds)")
# print(para)
# plt.legend()
# plt.show()


# Faire correspondre le coef de diffusion réel avec ceclui d'une marche aléatoire
# Contraite au nivea du nombre max de tour par seconde que l'ordinateur peur rendre, on a donc imposer tho
# Une fois qu'on a le coeff de diffusion on calcule, la probabilité pour qu'une bille rentre dans un stator
#