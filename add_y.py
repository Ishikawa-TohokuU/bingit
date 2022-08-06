import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter

#インプットの名前
inputfile = 'input.rd'

ss = mmps.Stream()
ss.import_file(inputfile, 'input')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd')
)

ratio = 8 #%

#flag = ss.sdat.particles['pos'][:,2] < 3
#print(flag)
# print(ss.sdat.particles['pos'])
#print(ss.sdat.particles['mask'])
#ss.sdat.particles['mask'] = np.where(flag,1,ss.sdat.particles['mask'])
#ss.sdat.particles['mask'][flag] = 1

flag = ss.sdat.particles['type'] == 1
print(flag)

c = Counter(flag)
zr = c[True]
print(zr)

y =math.ceil(0.01 * ratio * zr)
print(y)
if y % 2 == 1:
    y = y + 1
print(y)

oput = int(y / 2)
print(oput)

idxs = list(range(ss.sdat.total_particle))

#y_total = int((ss.sdat.particles['type'] == 1).sum() * 0.08)

i = 0

while i < y:
    idx = random.choice(idxs)
    if ss.sdat.particles['type'][idx] != 1:
        continue
    ss.sdat.particles['type'][idx] = 2
    i += 1

i = 0

while i < oput:
    idx = random.choice(idxs)
    if ss.sdat.particles['type'][idx] != 3:
        continue
    ss.sdat.particles['type'][idx] = 999
    i += 1

flag2 = ss.sdat.particles['type'] != 999
ss.sdat.trimming_particles(flag2, reindex=True)

#for i in range(1, y):
    #print(i)
   # k = random.choice(ss.sdat.particles['type'])
    #print(k)

#print(ss.sdat.type_to_mass[2])

#print(ss.sdat.particles['type'][8])

#print(ss.sdat.particles['mask'])


#ss.output_file('newinput.rd','input')
#ss.output_file('showdump.pos','dumppos')

particle = Counter(ss.sdat.particles['type'])
print(particle)

ss.output_file('newinput.rd','input')
ss.output_file('showdump.pos','dumppos',ss.sdat.particles.keys())