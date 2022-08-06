#!/usr/bin/env python3

import sys

from MolCop import mmpystream as mmps

from collections import Counter

#construct object
ss = mmps.Stream()

##################
#各方向に何倍圧縮・膨張するか
x = 0.96
y = 0.96
z = 0.96
##################

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

#import dumppos file
# ifn = sys.argv[1]
#import input file
# ss.import_file(ifn, 'input')
# print(f"Read file {ifn}")

total = ss.sdat.total_particle
print(total)
print(ss.sdat.cell)

for i in range(total):
    # print(ss.sdat.particles[i][0])
    ss.sdat.particles['pos'][i][0] = ss.sdat.particles['pos'][i][0] * x
    ss.sdat.particles['pos'][i][1] = ss.sdat.particles['pos'][i][1] * y
    ss.sdat.particles['pos'][i][2] = ss.sdat.particles['pos'][i][2] * z

ss.sdat.cell[0] = ss.sdat.cell[0] * x
ss.sdat.cell[1] = ss.sdat.cell[1] * y
ss.sdat.cell[2] = ss.sdat.cell[2] * z
ss.sdat.newcell[0] = ss.sdat.newcell[0] * x
ss.sdat.newcell[1] = ss.sdat.newcell[1] * y
ss.sdat.newcell[2] = ss.sdat.newcell[2] * z

print(ss.sdat.set_cellsize)
print(ss.sdat.newcell)

# ss.sdat.replicate_particles([x, y, z])

ss.sdat.shift_particles()
ss.sdat.wrap_particles()

particle = Counter(ss.sdat.particles['type'])
print(particle)

ofs = "newdump_from_" + ifn
ss.output_file('sizeinput', 'input')
ss.output_file(ofs, 'dumppos', ss.sdat.particles.keys())
