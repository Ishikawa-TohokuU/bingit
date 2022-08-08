#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

from MolCop import mmpystream as mmps

from collections import Counter

#construct object
ss = mmps.Stream()

##################
ifn = "inputfile"
auto_laich = "auto_laich"
src_dir = "src_laich"
#inputfile内に何個のinputがあるか
input_num = 13
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



for dir in range(input_num):
    newdir = "./laich_" + str(dir)
    os.mkdir(newdir)
    # os.chdir("../src_GA/" + ifn)
    shutil.copy("../src_GA/" + ifn + "/input." + str(dir), newdir)
    # print(ss.sdat.particles['pos'][24])
    
    # total = ss.sdat.total_particle
    # ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))
    
    
    # for i in range(total):
        # print(ss.sdat.particles[i][0])
        # ss.sdat.particles['pos'][i][0] = ss.sdat.particles['pos'][i][0] * size[dir]
        # ss.sdat.particles['pos'][i][1] = ss.sdat.particles['pos'][i][1] * size[dir]
        # ss.sdat.particles['pos'][i][2] = ss.sdat.particles['pos'][i][2] * size[dir]
    # print(ss.sdat.particles['pos'][24])

    # ss.sdat.cell[0] = ss.sdat.cell[0] * size[dir]
    # ss.sdat.cell[1] = ss.sdat.cell[1] * size[dir]
    # ss.sdat.cell[2] = ss.sdat.cell[2] * size[dir]
    # print(ss.sdat.newcell[0])
    # ss.sdat.newcell[0] = ss.sdat.newcell[0] * size[dir]
    # ss.sdat.newcell[1] = ss.sdat.newcell[1] * size[dir]
    # ss.sdat.newcell[2] = ss.sdat.newcell[2] * size[dir]
    # print(ss.sdat.newcell[0])

    # print(ss.sdat.set_cellsize)
    # print(ss.sdat.newcell)
    
    shutil.copy("./" + src_dir + "/para.rd", newdir)
    shutil.copy("./" + src_dir + "/config.rd", newdir)
    
    # os.chdir("..")
    
    # ss.sdat.shift_particles()
    # ss.sdat.wrap_particles()
    
    # ss.output_file('./' + newdir + '/input.rd', 'input')
    
    # print(size[dir])

# ss.sdat.replicate_particles([x, y, z])

# particle = Counter(ss.sdat.particles['type'])
# print(particle)

# ofs = "newdump_from_" + ifn
# ss.output_file(ofs, 'dumppos', ss.sdat.particles.keys())
