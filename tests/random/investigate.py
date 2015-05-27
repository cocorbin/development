__author__ = 'cocorbin'

#!/usr/bin/env python
''' Script to quickly investigate failed estimation runs.
'''
# standard library
import numpy as np

# project library
from   _randomInit  import *
from   _auxiliary   import *
import _tests       as lib

''' Request
'''
label, seed = 'C', 59334

''' Error Reproduction
'''
compileToolbox('fast')

test  = getattr(lib,'test' + label)

np.random.seed(seed)

test()
