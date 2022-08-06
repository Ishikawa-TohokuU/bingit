#!/usr/bin/env python3
import copy
import numpy as np

from MolCop import mmpystream as mmps

dstep = 1000
start_step = 0
total_step = 10000
#input_file = 'input.rd'
init_file = "dump.pos." + str(start_step)

ss = mmps.Stream()

#ss.import_file(input_file 'input')
ss.import_file(init_file, 'dumppos')
init_pos = copy.deepcopy(ss.sdat.particles['pos']) #元々の0step目のpos

ss.sdat.add_particles_property('shift_pos', float, 3)

elem_type = ss.sdat.particles['type']
type_flag = elem_type == 4 #type指定(ここでは3)
N = type_flag.sum()
#N = ss.sdat.total_particle #全原子対象のとき

bef_pos = copy.deepcopy(ss.sdat.particles['pos']) #元々のpos

print("Step MSD")
for step in range(start_step, total_step+1, dstep):

    ifs = 'dump.pos.' + str(step)
    ss.import_file(ifs, 'dumppos')
    pos = ss.sdat.particles['pos']

    cell = np.array(ss.sdat.newcell) #max-min

    shift_plus = (pos - bef_pos) < - cell * 0.5
    shift_minus = (pos - bef_pos) > cell * 0.5
    shift_pos = ss.sdat.particles['shift_pos']

    shift_pos += shift_plus
    shift_pos -= shift_minus

    pos += shift_pos * cell

    #normはベクトルの長さ
    msd =  (np.linalg.norm(pos[type_flag] - init_pos[type_flag]) ** 2) / N

    print(step, msd)

    bef_pos = copy.deepcopy(ss.sdat.particles['pos'])
