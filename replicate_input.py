#!/usr/bin/env python3

import sys

from MolCop import mmpystream as mmps

from collections import Counter

#construct object
ss = mmps.Stream()

##################
#各方向に何倍複製するか
x = 2
y = 2
z = 1
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

ss.sdat.replicate_particles([x, y, z])

ss.sdat.shift_particles()
ss.sdat.wrap_particles()

particle = Counter(ss.sdat.particles['type'])
print(particle)

ofs = "newdump_from_" + ifn
ss.output_file('newinput', 'input')
ss.output_file(ofs, 'dumppos', ss.sdat.particles.keys())
