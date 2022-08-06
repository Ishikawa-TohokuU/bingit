#!/usr/bin/env python3

import sys
import math

from MolCop import mmpystream as mmps

#construct object
ss = mmps.Stream()

if len(sys.argv) <= 1:
    print("No arguments are detected")
    sys.exit()

#import input files
if len(sys.argv) >= 2:
    ifn = sys.argv[1]
    ss.import_file(ifn, 'dumppos')
    print(f"Read input file {ifn}")

#read para.rd and set 
ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))

#import dumppos file
ifn = sys.argv[1]
#import input file
ss.import_file(ifn, 'dumppos')
print(f"Read file {ifn}")

ss.sdat.shift_particles()
ss.sdat.wrap_particles()

xmin = ss.sdat.cell[0]
ymin = ss.sdat.cell[1]
zmin = ss.sdat.cell[2]
xmax = ss.sdat.dcell[0]
ymax = ss.sdat.dcell[1]
zmax = ss.sdat.dcell[2]

# print(xmin)

for i in range(ss.sdat.total_particle):
    if (ss.sdat.particles['type'][i] == 4):
        if (xmin > ss.sdat.particles['pos'][i][0]):
            xmin = ss.sdat.particles['pos'][i][0]
        if (ymin > ss.sdat.particles['pos'][i][1]):
            ymin = ss.sdat.particles['pos'][i][1]
        if (zmin > ss.sdat.particles['pos'][i][2]):
            zmin = ss.sdat.particles['pos'][i][2]
        if (xmax < ss.sdat.particles['pos'][i][0]):
            xmax = ss.sdat.particles['pos'][i][0]
        if (ymax < ss.sdat.particles['pos'][i][1]):
            ymax = ss.sdat.particles['pos'][i][1]
        if (zmax < ss.sdat.particles['pos'][i][2]):
            zmax = ss.sdat.particles['pos'][i][2]
            

dx = xmax - xmin
dy = ymax - ymin
h = zmax - zmin
theta_x = 2 * math.atan((2 * h) / dx) * (180 / math.pi)
theta_y = 2 * math.atan((2 * h) / dy) * (180 / math.pi)

print('dx = ', dx)
print('dy = ', dy)
print('h = ', h)
print('θx = ', theta_x)
print('θy = ', theta_y)
