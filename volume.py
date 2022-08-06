from pickle import TRUE
import numpy as np
import math
import random
from MolCop import mmpystream as mmps
from collections import Counter


ifn = 'dump.pos.60000'

ss = mmps.Stream()
ss.import_file(ifn, 'dumppos')

xsize = ss.sdat.newcell[0]
ysize = ss.sdat.newcell[1]
zsize = ss.sdat.newcell[2]
volume = xsize * ysize * zsize
print(xsize)
print(ysize)
print(zsize)
print("volume =", volume)





