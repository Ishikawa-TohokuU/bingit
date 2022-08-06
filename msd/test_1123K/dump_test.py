#!/usr/bin/env python3

import sys
import numpy as np

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

dump_np = []
step = 0
fopen = open("dump.pos." + str(step), "r")
lines = fopen.readlines()
lines = lines[9:]
print(lines[0])
print(type(lines))

ss.sdat.add_particles_property('number', int,  1)

print(ss.sdat.particles)
number = []

i = 0
for line in lines:
    line_split = line.split()
    print(line_split[0])
    # ss.sdat.particles['number'][i] = line_split[0]
    number = line_split[0]
    line_list = np.matrix(line_split)
    # print(line_list.shape)
    # dump_np = np.append(dump_np, line_split)
    # print(dump_np.reshape(i + 1, 9))
    i += 1

print(ss.sdat.particles)

ss.sdat.shift_particles()
ss.sdat.wrap_particles()

# ofs = "newcar_from_" + ifn
# ss.output_file(ofs, 'car')
