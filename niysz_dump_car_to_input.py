#!/usr/bin/env python3

import sys
from collections import Counter
from MolCop import mmpystream as mmps

#construct object
ss = mmps.Stream()
ss2 = mmps.Stream()

if len(sys.argv) <= 1:
    print("No arguments are detected")
    sys.exit()

print(sys.argv)

#import input files
if len(sys.argv) >= 3:
    ifn = sys.argv[1]
    ss.import_file(ifn, 'dumppos')
    print(f"Read input file {ifn}")
    ifn2 = sys.argv[2]
    ss2.import_file(ifn2, 'car')
    print(f"Read input file {ifn2}")

print(sys.argv)

#read para.rd and set 
ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))
ss2.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))

ss.sdat.shift_particles()
ss.sdat.wrap_particles()

YSZ_xcenter = (ss.sdat.cell[0] - ss.sdat.dcell[0]) / 2
YSZ_ycenter = (ss.sdat.cell[1] - ss.sdat.dcell[1]) / 2

Ni_zmin = ss2.sdat.particles['pos'][0][2]
for i in range(ss2.sdat.total_particle):
    if Ni_zmin > ss2.sdat.particles['pos'][i][2]:
        Ni_zmin = ss2.sdat.particles['pos'][i][2]
print(Ni_zmin)

Ni_center = [(ss2.sdat.cell[0] - ss2.sdat.dcell[0]) / 2,(ss2.sdat.cell[1] - ss2.sdat.dcell[1]) / 2,(ss2.sdat.cell[2] - ss2.sdat.dcell[2]) / 2 ]
print(Ni_center)

YSZ_zmax = ss.sdat.particles['pos'][0][2]
for i in range(ss.sdat.total_particle):
    if YSZ_zmax < ss.sdat.particles['pos'][i][2]:
        YSZ_zmax = ss.sdat.particles['pos'][i][2]
print(YSZ_zmax)

Ni_newcenter = [YSZ_xcenter, YSZ_ycenter, (YSZ_zmax + 2 + (Ni_center[2] - Ni_zmin))]
print(Ni_newcenter)

cell = [[0, ss.sdat.newcell[0]], [0, ss.sdat.newcell[1]], [0, ss.sdat.newcell[2]]]
ss2.sdat.set_cellsize(cell)
print(ss2.sdat.newcell)

Ni_move = [Ni_newcenter[0] - Ni_center[0], Ni_newcenter[1] - Ni_center[1], Ni_newcenter[2] - Ni_center[2]]
# Ni_move = [Ni_newcenter[0] - Ni_center[0], Ni_newcenter[1] - Ni_center[1], 100]
print(Ni_move)

ss2.sdat.shift_particles(Ni_move)

Ni_zmin = ss2.sdat.particles['pos'][0][2]
for i in range(ss2.sdat.total_particle):
    if Ni_zmin > ss2.sdat.particles['pos'][i][2]:
        Ni_zmin = ss2.sdat.particles['pos'][i][2]
print(Ni_zmin)

for i in range(ss2.sdat.total_particle):
    ss2.sdat.particles['type'][i] = ss.sdat.elem_to_type['Ni']

ss.sdat.concate_particles(ss2.sdat.particles)

del ss.sdat.particles["element"]

print(ss2.sdat.particles['type'])
print(ss2.sdat.elem_to_type)

# print(ss.sdat.particles)

particle = Counter(ss.sdat.particles['type'])
print(particle)

# print(ss2.sdat.particles)


ofs = "newinput.rd"
ss.output_file(ofs, 'input')
ss.output_file('showdump.pos', 'dumppos', ss.sdat.particles.keys())

# ss3 = mmps.Stream()
# ss3.import_file('showdump.pos', 'dumppos')
# del ss3.sdat.particles["mask"]
# print(ss3.sdat.particles)

# ss3.output_file('showdump.pos2', 'dumppos', ss3.sdat.particles.keys())