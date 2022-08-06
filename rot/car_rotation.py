#!/usr/bin/env python3

import sys
import math
import numpy as np

from MolCop import mmpystream as mmps


#########Parameters##########

rot_angle = 45 # degree
rot_angle_y = 35

#############################

def sin(degree):
    rot_angle_radian = math.radians(degree)
    sin_theta = math.sin(rot_angle_radian)
    return sin_theta

def cos(degree):
    rot_angle_radian = math.radians(degree)
    cos_theta = math.cos(rot_angle_radian)
    return cos_theta

#construct object
ss = mmps.Stream()

if len(sys.argv) <= 1:
    print("No arguments are detected")
    sys.exit()

#import input files
if len(sys.argv) >= 2:
    ifn = sys.argv[1]
    ss.import_file(ifn, 'input')
    print(f"Read input file {ifn}")

#read para.rd and set 
ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))

print(ss.sdat.particles)

xmax = ss.sdat.cell[0]
ymax = ss.sdat.cell[1]
zmax = ss.sdat.cell[2]
center = [xmax/2, ymax/2, zmax/2]

# print(xmax)
# print(ymax)
# print(zmax)
# print(center)

total = ss.sdat.total_particle

# print(sin(rot_angle))
rot_x = np.matrix([[1, 0, 0],
                  [0, cos(rot_angle), -sin(rot_angle)],
                  [0, sin(rot_angle), cos(rot_angle)]])

rot_y = np.matrix([[cos(rot_angle_y), 0, sin(rot_angle_y)],
                  [0, 1, 0],
                  [-sin(rot_angle_y), 0, cos(rot_angle_y)]])

rot_z = np.matrix([[cos(rot_angle), -sin(rot_angle), 0],
                  [sin(rot_angle), cos(rot_angle), 0],
                  [0, 0, 1]])

ss.sdat.shift_particles(-1/2 * float(ss.sdat.cell[0]))

pos = np.matrix(ss.sdat.particles['pos'])

shift_pos = 2 * center


print(pos[0])


for i in range(total):
    pos_T = np.matrix([[pos.T[0, i]],
                      [pos.T[1, i]],
                      [pos.T[2, i]]])
    newpos = np.dot(rot_x, pos_T)
    newpos = np.dot(rot_y, newpos)
    # newpos = np.dot(rot_z, newpos)
    # print(newpos)
    for k in range(3):
        ss.sdat.particles['pos'][i][k] = float(newpos[k, 0])
        
print(pos[0])

print(ss.sdat.particles['pos'][0])

ss.sdat.shift_particles(1/2 * float(ss.sdat.cell[0]))

# ss.sdat.wrap_particles()
print(ss.sdat.particles)

ss.output_file("rotdump", 'dumppos', ss.sdat.particles.keys())
ss.output_file("rotcar", 'car')
