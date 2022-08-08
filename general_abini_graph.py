#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from MolCop import mmpystream as mmps

from collections import Counter

#construct object
# ss = mmps.Stream()

##################
abini = "abini.dat"
laich_out = "out"
cellratio = 640
#inputfile内の構造の数
input_num = 13
#保存するファイルの名前
image_name = "abini_MD"
##################

# if len(sys.argv) <= 1:
#     print("No arguments are detected")
#     sys.exit()


# #import input files
# if len(sys.argv) >= 2:
#     ifn = sys.argv[1]
#     ss.import_file(ifn, 'input')
#     print(f"Read input file {ifn}")

#read para.rd and set 

df = pd.read_csv(abini, delim_whitespace=True) #不規則なスペース区切りをCSVで正しく読み込む
df['MD/cellratio'] = 0.0
df['MD_offset'] = 0.0
print(df)

for dir in range(input_num):
    print(dir)
    laich_dir = "laich_" + str(dir)
    os.chdir(laich_dir)
    
    ss = mmps.Stream()
    ss.import_file(laich_out, 'out')
    energy = ss.sdat.TotalE[0] / cellratio
    print(energy)
    df['MD/cellratio'][dir] = energy
    
    os.chdir("..")
    
MD_min = df['MD/cellratio'].min()
print("MD_min = " + str(MD_min))

for dir in range(input_num):
    df["MD_offset"][dir] = df["MD/cellratio"][dir] - (MD_min)

print(df)

# df.plot(x='change', y='Ef_offset')
# df.plot(x='change', y='MD_offset')

df.plot(x='change', y=['Ef_offset', 'MD_offset'])
plt.savefig(image_name)