#!/usr/bin/env python3

import sys
from collections import Counter

from MolCop import mmpystream as mmps

#construct object
ss = mmps.Stream()

if len(sys.argv) <= 1:
    print("No arguments are detected")
    sys.exit()

#import input name
ifn = sys.argv[1]

#read element type from reaxff paramerter file
ss.sdat.set_elem_to_type(mmps.get_elem_to_type("para.rd"))

#import input file
ss.import_file(ifn, 'car')


particle = Counter(ss.sdat.particles['type'])
print(particle)

ss.output_file('newinput', 'input')

