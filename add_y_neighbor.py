from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter

#インプットの名前
inputfile = 'input.rd'
dumpbondfile = 'dump.bond.0'
Zrtype = 1
Ytype = 2
Otype = 3
ratio = 8 #%

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

flag = ss.sdat.particles['type'] == Zrtype
print(flag)

c = Counter(flag)
zr = c[True]
print(zr)

flagO = ss.sdat.particles['type'] == Otype
print(flagO)

co = Counter(flagO)
o = co[True]

y =math.ceil((1/(100 - ratio)) * (2 * ratio) * zr)
print(y)
if y % 2 == 1:
    y = y + 1
print('y=', y)

# oput = int(y / 2)
# print(oput)

idxs = list(range(ss.sdat.total_particle))

ss.sdat.create_connect_list(0.3)
connect_list = ss.sdat.connect_list

# top = np.array([r[0] for r in connect_list])

#y_total = int((ss.sdat.particles['type'] == 1).sum() * 0.08)

flag2= [True for _ in range(ss.sdat.total_particle)]

i = 0
k = 1
idxy = []

while i < y:
    idx = random.choice(idxs)
    if ss.sdat.particles['type'][idx] != Zrtype:
        # print(i)
        continue
    ss.sdat.particles['type'][idx] = Ytype
    idxy.append(idx)
    zr = zr - 1
    if i % 2 == 0:
        if o > 2 * zr + 3 * y / 2:
            while k == 1:
                idx2 = random.choice(ss.sdat.connect_list[idx])
                if ss.sdat.particles['type'][idx2] == Otype:
                    if flag2[idx2] == True:
                        flag2[idx2]  = False
                        k = 0
                        o = o - 1
                        break
    i += 1
    k = 1

print('o=', o)

while o > 2 * zr + 3 * y / 2:
    idx3 = random.choice(ss.sdat.connect_list[random.choice(idxy)])
    if ss.sdat.particles['type'][idx3] == Otype:
        if flag2[idx3] == True:
            flag2[idx3]  = False
            o = o - 1
            print(o)

print(zr)
print(y)
print('o=', o)
print(2 * zr + 3 * y / 2)
# print(flag2)
ss.sdat.trimming_particles(flag2, reindex=True)


# while i < y:
#     idx = random.choice(idxs)
#     if ss.sdat.particles['type'][idx] != Zrtype:
#         if i % 2 == 0:
#                 connect = np.where(top == i)
#                 print(connect)
#                 if len(connect) == 0:
#                     continue
#                 gyo = connect[0][0]
#                 for j in range(0, len(connect_list[gyo])):
#                     if ss.sdat.particles['type'][connect_list[gyo][j]] == Otype:
#                         ss.sdat.particles['mask'][connect_list[gyo][j]] = 999
#                         print(connect_list[gyo])
#                         print(connect_list[gyo][j])
#                         break
#         continue
#     ss.sdat.particles['type'][idx] = Ytype
#     print('i=', i)
#     i += 1

i = 0

# while i < oput:
    # idx = random.choice(idxs)
    # if ss.sdat.particles['type'][idx] != 3:
        # continue
    # ss.sdat.particles['type'][idx] = 999
    # i += 1

# flag2 = ss.sdat.particles['type'] != 999

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