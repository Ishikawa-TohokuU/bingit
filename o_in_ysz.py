#!/usr/bin/env python3
import copy
from sqlite3 import connect
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from MolCop import mmpystream as mmps

#################################
dstep = 100000
start_step = 0
total_step = 1000000
#input_file = 'input.rd'
init_pos = "dump.pos." + str(start_step)
init_bond = "dump.bond." + str(start_step)
image_name = "O_in_YSZ"
#################################

ss = mmps.Stream()

#ss.import_file(input_file 'input')
ss.import_file(init_pos, 'dumppos')
ss.import_file(init_bond, 'dumpbond')
ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))

o_type = ss.sdat.elem_to_type["O"]
y_type = ss.sdat.elem_to_type["Y"]
zr_type = ss.sdat.elem_to_type["Zr"]
elem_type = ss.sdat.particles['type']
type_flag = elem_type == o_type #type指定(ここでは3)
o_number = type_flag.sum()
total = ss.sdat.total_particle 

layer_list = []
for step in range(start_step, total_step+1, dstep):
    print("step = ", step)

    ifp = 'dump.pos.' + str(step)
    ss.import_file(ifp, 'dumppos')
    ifb = 'dump.bond.' + str(step)
    ss.import_file(ifb, 'dumpbond')

    ss.sdat.create_connect_list(0.3)
    connect_list = ss.sdat.connect_list

    z_min = ss.sdat.particles["pos"][0][2]
    ysz_z_max = 0
    ysz_flag = [False] * total
    # print(ysz_flag)
    # print(ss.sdat.particles["type"] == 3)
    for i in range(total):
        if ss.sdat.particles["pos"][i][2] < z_min and ss.sdat.particles["type"][i] == o_type:
            z_min = ss.sdat.particles["pos"][i][2]
        if type_flag[i] == True:
            con_num = len(connect_list[i])
            y_or_zr = 0
            for k in range(con_num):
                if (ss.sdat.particles["type"][connect_list[i][k]] == y_type) or ss.sdat.particles["type"][connect_list[i][k]] == zr_type:
                    y_or_zr += 1
                    if y_or_zr == 3:
                        ysz_flag[i] = True
                        if ss.sdat.particles["pos"][i][2] > ysz_z_max:
                            ysz_z_max = ss.sdat.particles["pos"][i][2]
                            # print(ss.sdat.particles["pos"][i])
                            # print(connect_list[i])
                            # ysz_flag.append(True)
                            break
    print(z_min, ysz_z_max)

    ysz_thick = ysz_z_max - z_min

    ysz_0 = z_min
    ysz_1 = z_min + (ysz_thick / 5)
    ysz_2 = z_min + 2 * (ysz_thick / 5)
    ysz_3 = z_min + 3 * (ysz_thick / 5)
    ysz_4 = z_min + 4 * (ysz_thick / 5)
    ysz_5 = z_min + 5 * (ysz_thick / 5)

    print(ysz_1-ysz_0, ysz_2-ysz_1, ysz_3-ysz_2, ysz_4-ysz_3, ysz_5-ysz_4)

    pos = ss.sdat.particles['pos']

    layer_1 = 0
    layer_2 = 0
    layer_3 = 0
    layer_4 = 0
    layer_5 = 0

    for i in range(total):
        if ysz_flag[i] == True:
            if pos[i][2] <= ysz_1:
                layer_1 += 1
            if ysz_1 < pos[i][2] and pos[i][2] <= ysz_2:
                layer_2 += 1
            if ysz_2 < pos[i][2] and pos[i][2] <= ysz_3:
                layer_3 += 1
            if ysz_3 < pos[i][2] and pos[i][2] <= ysz_4:
                layer_4 += 1
            if ysz_4 < pos[i][2] and pos[i][2] <= ysz_5:
                layer_5 += 1
    
    print("layer_1: ", layer_1)
    print("layer_2: ", layer_2)
    print("layer_3: ", layer_3)
    print("layer_4: ", layer_4)
    print("layer_5: ", layer_5)

    layer_list_step = []
    layer_list_step.append(layer_1)
    layer_list_step.append(layer_2)
    layer_list_step.append(layer_3)
    layer_list_step.append(layer_4)
    layer_list_step.append(layer_5)

    layer_list.append(layer_list_step)

print(layer_list)

dump_num = int((total_step - start_step) / dstep)

plot_idx = []
for n in range(dump_num+ 1):
    plot_idx.append(str(start_step + (n * dstep)))
    # if n == dump_num:
    # plot = plot + "'" + str(start_step + (n * dstep)) + "', "

df = pd.DataFrame(np.arange(len(plot_idx) * 6).reshape(len(plot_idx), 6), columns=['timestep', 'layer_1', 'layer_2', 'layer_3', 'layer_4', 'layer_5'], index=plot_idx)
# print(df)

df['timestep'] = plot_idx
df['timestep'] = df['timestep'].astype(int)

for time in range(dump_num + 1):
    df['layer_1'][time] = layer_list[time][0]
    df['layer_2'][time] = layer_list[time][1]
    df['layer_3'][time] = layer_list[time][2]
    df['layer_4'][time] = layer_list[time][3]
    df['layer_5'][time] = layer_list[time][4]


print(df)

# plt.plot(df)
df.plot(x='timestep', y=['layer_1', 'layer_2', 'layer_3', 'layer_4', 'layer_5'])
plt.show()
plt.savefig(image_name)

particle = Counter(ss.sdat.particles['type'])
print(particle)
