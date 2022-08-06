from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter

inputfile = 'input.rd'
carfile = 'niysz_c16_o8192.car'
xyzfile = 'water.xyz'
dumpbondfile = 'dump.bond.0'
Zrtype = 1
Ytype = 2
Otype = 3
Htype = 5
ratio = 8 #%
upfrac = 0.9
btfrac = 0.1
BondOrder = 0.3


ss = mmps.Stream()
ssx = mmps.Stream()
ss.import_file(inputfile, 'input')
#ss.import_file(carfile, 'car')
ssx.import_file(xyzfile, 'xyz')
ss.import_file(dumpbondfile, 'dumpbond')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd'))
#ssx.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd'))

for i in range(ssx.sdat.total_particle):
    if ssx.sdat.particles['type'][i] == 1:
        ssx.sdat.particles['type'][i] = ss.sdat.elem_to_type['H']
    if ssx.sdat.particles['type'][i] == 2:
        ssx.sdat.particles['type'][i] = ss.sdat.elem_to_type['O']

print(ss.sdat.particles)
print(ssx.sdat.particles)
print(ssx.sdat.particles['type'][1])

ss.sdat.concate_particles(ssx.sdat.particles)

print(ss.sdat.total_particle)

particle = Counter(ss.sdat.particles['type'])
print(particle)

ss.output_file('xyzinput.rd','input')
#ss.output_file('newcar.car','car',ss.sdat.particles.keys())
ss.output_file('xyzinputdump.pos','dumppos',ss.sdat.particles.keys())