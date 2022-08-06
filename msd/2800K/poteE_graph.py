from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
# ここにグラフを描画してファイルに保存する処理


ifn = 'out'

ss = mmps.Stream()
ss.import_file(ifn, 'out')

print(ss.sdat.STEP[1300])
print(ss.sdat.TEMP[1301])
print(ss.sdat.STEP[1300] + ss.sdat.TEMP[1301])
print(ss.sdat.MDstep)

# print(len(ss.sdat.STEP))
# print(len(ss.sdat.PotentialE))

plt.plot(ss.sdat.STEP, ss.sdat.PotentialE);

plt.savefig("PotentialE.png")
# plt.show()



