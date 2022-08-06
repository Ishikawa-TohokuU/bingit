import numpy as np
from MolCop import mmpystream as mmps

#インプットの名前
inputfile = 'input.rd'

ss = mmps.Stream()
ss.import_file(inputfile, 'input')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type('para.rd')
)

zmin = ss.sdat.particles['pos'][0][2]
zmax = ss.sdat.particles['pos'][0][2]

for i in range(0,ss.sdat.total_particle):
    print(ss.sdat.particles['pos'][i][2])
    if zmin > ss.sdat.particles['pos'][i][2]:
        zmin = ss.sdat.particles['pos'][i][2]
    if zmax < ss.sdat.particles['pos'][i][2]:
        zmax = ss.sdat.particles['pos'][i][2]
    i = i + 1

flag = ss.sdat.particles['pos'][:,2] - zmin < 4
print(flag)
# print(ss.sdat.particles['pos'])
print(ss.sdat.particles['mask'])
ss.sdat.particles['mask'] = np.where(flag,1,ss.sdat.particles['mask'])
#ss.sdat.particles['mask'][flag] = 1

print(ss.sdat.particles['mask'])


ss.output_file('maskinput.rd','input')
#ss.output_file('showdump.pos','dumppos')
