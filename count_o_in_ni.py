import numpy as np
from collections import Counter
from MolCop import mmpystream as mmps

#####################
posfile = 'dump.pos.1000000'
bondfile = 'dump.bond.1000000'
Bond_Order = 0.3
# Ni_zmin = 55
#####################


ss = mmps.Stream()
ss.import_file(posfile, 'dumppos')
ss.import_file(bondfile, 'dumpbond')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd'))

for i in range(ss.sdat.total_particle):
    if ss.sdat.particles['type'][i] == ss.sdat.elem_to_type["Ni"]:
        Ni_zmin = ss.sdat.particles['pos'][0][2]
        Ni_zmax = ss.sdat.particles['pos'][0][2]
        break

flag = ss.sdat.particles['type'] == ss.sdat.elem_to_type['O']
print(flag)
print(flag[0])
ss.sdat.create_connect_list(Bond_Order)
connect_list = ss.sdat.connect_list

count = 0
Ni_flag = 0
Zr_flag = 0
ss.sdat.add_particles_property("mask", _dtype=int, dim=1)

for i in range(ss.sdat.total_particle):
    if (flag[i] == True) and (ss.sdat.particles['pos'][i][2] > Ni_zmin):
        print(connect_list[i])
        connect_number = len(connect_list[i])
        for connect in range(connect_number):
            if ss.sdat.particles['type'][connect_list[i][connect]] == ss.sdat.elem_to_type['Ni']:
                Ni_flag = 1
            if ss.sdat.particles['type'][connect_list[i][connect]] == ss.sdat.elem_to_type['Zr']:
                Zr_flag = 1
        if Ni_flag == 1 and Zr_flag ==0:
            count += 1
        Ni_flag = 0
        Zr_flag = 0
        
print("Number of O in Ni: ", count)

# print(connect_list[35068])
# for i in range(len(connect_list[35068])):
#     print(ss.sdat.particles['type'][connect_list[35068][i]])

particle = Counter(ss.sdat.particles['type'])
print(particle)

# flag = ss.sdat.particles['pos'][:,2] - zmin < 4
# print(flag)
# print(ss.sdat.particles['pos'])
# print(ss.sdat.particles['mask'])
# ss.sdat.particles['mask'] = np.where(flag,1,ss.sdat.particles['mask'])
#ss.sdat.particles['mask'][flag] = 1

# print(ss.sdat.particles['mask'])


# ss.output_file('maskinput.rd','input')
#ss.output_file('showdump.pos','dumppos')
