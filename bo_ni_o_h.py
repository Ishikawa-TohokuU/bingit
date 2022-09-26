#!/usr/bin/env python3
import sys
import numpy as np
from KudoCop.SimulationDat import SimulationDat
from KudoCop.SimulationDats import SimulationDats
from tqdm import tqdm, trange
import pandas as pd
import matplotlib.pyplot as plt
from time import time
pd.set_option("display.max_columns", 100)

#####################################
skip_num = 1
start_step = 0
onestep = 100000
total_step = 800000

#####################################
skip_rows = 0

step_nums = range(start_step, total_step + onestep, onestep)
steps = int(((total_step - start_step) / onestep) + 1)
try:
    skip_num = int(sys.argv[1])
except:
    pass
sdats = SimulationDats(step_nums = step_nums, skip_num=skip_num)
def condition(sdats, skip_idx):
    skip_idx = 0
    return sdats.atoms[skip_idx]['z'] >= 52


bo_ni_ave = []
bo_ni_o_ave = []
bo_ni_h_ave = []
bo_ni_all_ave = []
ni_num_total = []
ni_o_num_total = []
ni_h_num_total = []
for step in range(steps):
    print('step = ', step)
    bo_ni_total = 0
    bo_ni_num = 0
    bo_ni_o_total = 0
    bo_ni_o_num = 0
    bo_ni_h_total = 0
    bo_ni_h_num = 0
    connect_list = sdats.get_connect_lists(0.3)[step]
    bo_list = sdats.bondorder_lists[step]
    bo_connect_list = sdats.bondorder_connect_lists[step]
    # print(connect_list)
    for id in range(sdats.get_total_atoms()):
        # print(id)
        if sdats.atoms[step]['type'][id] == sdats.atom_symbol_to_type['Ni']:
            # print('Ni', step)
            for con in range(len(connect_list[id])):
                con_id = connect_list[id][con]
                if sdats.atoms[step]['type'][con_id] == sdats.atom_symbol_to_type['Ni']:
                    for bolist in range(len(bo_connect_list[id])):
                        if bo_connect_list[id][bolist] == con_id:
                            for con_conlist in range(len(connect_list[con_id])):
                                if sdats.atoms[step]['type'][connect_list[con_id][con_conlist]] == sdats.atom_symbol_to_type['O']:
                                    bo_ni_o_total += bo_list[id][con][3]
                                    bo_ni_o_num += 1
                                    break
                                if sdats.atoms[step]['type'][connect_list[con_id][con_conlist]] == sdats.atom_symbol_to_type['H']:
                                    bo_ni_h_total += bo_list[id][con][3]
                                    bo_ni_h_num += 1
                                    break
                            bo_ni_total += bo_list[id][con][3]
                            bo_ni_num += 1
                            # print(bo_connect_list[id][bolist], con_id)
    
    if bo_ni_num != 0:
        bo_ni_ave.append(bo_ni_total / bo_ni_num)
    else:
        bo_ni_ave.append(0.0)

    if bo_ni_o_num != 0:
        bo_ni_o_ave.append(bo_ni_o_total / bo_ni_o_num)
    else:
        bo_ni_o_ave.append(0.0)

    if bo_ni_h_num != 0:
        bo_ni_h_ave.append(bo_ni_h_total / bo_ni_h_num)
    else:
        bo_ni_h_ave.append(0.0)

    ni_num_total.append(bo_ni_num)
    ni_o_num_total.append(bo_ni_o_num)
    ni_h_num_total.append(bo_ni_h_num)

    bo_ni_all = bo_ni_total + bo_ni_o_total + bo_ni_h_total
    bo_ni_all_num = bo_ni_num + bo_ni_o_num + bo_ni_h_num
    bo_ni_all_ave.append(bo_ni_all / bo_ni_all_num)

step_row = []
for step in step_nums:
    step_row.append(step)

pd.set_option('display.unicode.east_asian_width', True)

df = pd.DataFrame(
    data={'BO_ni_ave': bo_ni_ave,
          'BO_ni_o_ave': bo_ni_o_ave,
          'BO_ni_h_ave': bo_ni_h_ave,
          'BO_ni_all_ave': bo_ni_all_ave,
          'ni_num_total': ni_num_total,
          'ni_o_num_total': ni_o_num_total,
          'ni_h_num_total': ni_h_num_total},
    index = step_row
)

df = df.round({'BO_ni_ave': 3, 'BO_ni_o_ave': 3, 'BO_ni_h_ave': 3, 'BO_ni_all_ave': 3})

print(df)
print('ni_num_total = ', ni_num_total)
print('ni_o_num_total = ', ni_o_num_total)
print('ni_h_num_total = ', ni_h_num_total)

df[['BO_ni_ave', 'BO_ni_o_ave', 'BO_ni_h_ave', 'BO_ni_all_ave']].plot()
plt.savefig('BO_Ni_O_H.png')
plt.show()

df.to_csv("BO_Ni_O_H.csv", sep='\t', index=False)

# print(sdats.bondorder_lists[0][1][0][3])
# print(sdats.get_connect_lists(0.3)[step][1])
