#!/usr/bin/env python3
import copy
import numpy as np

from MolCop import mmpystream as mmps

dstep = 10000
start_step = 0
total_step = 100000
#input_file = 'input.rd'
init_file = "dump.pos." + str(start_step)

ss = mmps.Stream()

#ss.import_file(input_file 'input')
ss.import_file(init_file, 'dumppos')
init_pos = copy.deepcopy(ss.sdat.particles['pos']) #元々の0step目のpos

ss.sdat.add_particles_property('shift_pos', float, 3)

ss.sdat.add_particles_property('number', int, 1)
for i in range(ss.sdat.total_particle):
    ss.sdat.particles['number'][i] = i + 1

elem_type = ss.sdat.particles['type']
type_flag = elem_type == 4 #type指定(ここでは3)
N = type_flag.sum()
#N = ss.sdat.total_particle #全原子対象のとき

bef_pos = copy.deepcopy(ss.sdat.particles['pos']) #元々のpos

# dump_np = []

pre_number = list(range(ss.sdat.total_particle))
num = []
# print(pre_number)

print("Step MSD")
for step in range(start_step, total_step+1, dstep):
    
    # dump_np = np.matrix()
    fopen = open("dump.pos." + str(step), "r")
    lines = fopen.readlines()
    lines = lines[9:]
    # print(lines[0])
    # print(type(lines))
    
    i = 0
    for line in lines:
        line_split = line.split()
        number = num.append(line_split[0])
        i += 1
    
    # print(number)
    
    # for line in lines:
    #     line_split = line.split()
    #     line_list = np.matrix(line_split)
    #     print(line_list[0])
    #     dump_np = np.append(dump_np, line_list)
    #     dump_np = dump.np.reshape(i + 1, 9)
    #     # print(line_split[0])
    #     i += 1


    ifs = 'dump.pos.' + str(step)
    ss.import_file(ifs, 'dumppos')
    pos = ss.sdat.particles['pos']
    
    # print('step',step, ss.sdat.particles['id'])

    cell = np.array(ss.sdat.newcell) #max-min

    shift_plus = (pos - bef_pos) < - cell * 0.5
    shift_minus = (pos - bef_pos) > cell * 0.5
    shift_pos = ss.sdat.particles['shift_pos']

    shift_pos += shift_plus
    shift_pos -= shift_minus

    pos += shift_pos * cell
    
    # print(pos)

    #normはベクトルの長さ
    msd =  (np.linalg.norm(pos[type_flag] - init_pos[type_flag]) ** 2) / N
    msd_per_step =  msd / step
    # msd_per_step =  float(msd) / float(step + 1)

    print(step, msd)
    # print(ss.sdat.particles["shift_pos"])

    bef_pos = copy.deepcopy(ss.sdat.particles['pos'])
