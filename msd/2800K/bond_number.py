from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter

#インプットの名前
inputfile = 'input.rd'
dumpbondfile = 'dump.bond.20000'
Zrtype = 1
Ytype = 2
Otype = 3
Nitype = 4
ratio = 8 #%
bond_order = 0.1

ss = mmps.Stream()
ss.import_file(inputfile, 'input')
ss.import_file(dumpbondfile, 'dumpbond')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd')
)

#flag = ss.sdat.particles['pos'][:,2] < 3
#print(flag)
# print(ss.sdat.particles['pos'])
#print(ss.sdat.particles['mask'])
#ss.sdat.particles['mask'] = np.where(flag,1,ss.sdat.particles['mask'])
#ss.sdat.particles['mask'][flag] = 1

flag = ss.sdat.particles['type'] == Nitype
# print(flag)
Ni_number = Counter(flag)
print(Ni_number)

ss.sdat.create_connect_list(bond_order)
connect_list = ss.sdat.connect_list
print(connect_list)
bond_number = []
k = 0

for i in range(ss.sdat.total_particle):
    if flag[i] == True:
        bond_number.append(len(connect_list[i]))
        k += 1

print(bond_number)

# oput = int(y / 2)
# print(oput)

idxs = list(range(ss.sdat.total_particle))



flag2= [True for _ in range(ss.sdat.total_particle)]

i = 0
k = 1

# print(flag2)
ss.sdat.trimming_particles(flag2, reindex=True)


i = 0

particle = Counter(ss.sdat.particles['type'])
print(particle)

# ss.output_file('newinput.rd','input')
# ss.output_file('showdump.pos','dumppos',ss.sdat.particles.keys())