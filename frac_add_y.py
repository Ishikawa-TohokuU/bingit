from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter

inputfile = 'input.rd'
dumpbondfile = 'dump.bond.0'
Zrtype = 1
Ytype = 2
Otype = 3
ratio = 8 #%
upfrac = 0.9
btfrac = 0.1
BondOrder = 0.3


ss = mmps.Stream()
ss.import_file(inputfile, 'input')
ss.import_file(dumpbondfile, 'dumpbond')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd'))

flag = ss.sdat.particles['type'] == Zrtype
print(flag)

c = Counter(flag)
zr = c[True]
#print(zr)

y =math.ceil(0.01 * ratio * zr)
#print(y)
if y % 2 == 1:
    y = y + 1
#print(y)

print(ss.sdat.total_particle)

zmin = ss.sdat.particles['pos'][0][2]
zmax = ss.sdat.particles['pos'][0][2]

for i in range(0,ss.sdat.total_particle):
    print(ss.sdat.particles['pos'][i][2])
    if zmin > ss.sdat.particles['pos'][i][2]:
        zmin = ss.sdat.particles['pos'][i][2]
    if zmax < ss.sdat.particles['pos'][i][2]:
        zmax = ss.sdat.particles['pos'][i][2]
    i = i + 1

atomthick = zmax - zmin
zfrac_up = zmin + upfrac * atomthick
zfrac_bt = zmax + btfrac * atomthick


idxs = list(range(ss.sdat.total_particle))

ss.sdat.create_connect_list(BondOrder)
connect_list = ss.sdat.connect_list

flag2= [True for _ in range(ss.sdat.total_particle)]

i = 0
k = 1

while i < y:
    idx = random.choice(idxs)
    if ss.sdat.particles['type'][idx] != Zrtype:
        print(i)
        continue
    ss.sdat.particles['type'][idx] = Ytype
    if i % 2 == 0:
        while k == 1:
            idx2 = random.choice(ss.sdat.connect_list[idx])
            if ss.sdat.particles['type'][idx2] == Otype:
                if flag2[idx2] == True:
                    if ss.sdat.particles['pos'][i][2] > zfrac_up or ss.sdat.particles['pos'][i][2] < zfrac_bt:
                        flag2[idx2]  = False
                        k = 0
                        break
    i += 1
    k = 1


print(zr)
print(y)
# print(flag2)
ss.sdat.trimming_particles(flag2, reindex=True)

particle = Counter(ss.sdat.particles['type'])
print(particle)

print(zmax, zmin)

ss.output_file('newinput.rd','input')
ss.output_file('showdump.pos','dumppos',ss.sdat.particles.keys())