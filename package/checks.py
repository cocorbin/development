""" This module shows outlines the basic checks that test the random
    generation of the initialization files.
"""

import sys
import os

sys.path.insert(0, '/home/peisenha/grmToolbox/development/package/tests'
                   '/random/modules')


sys.path.insert(0, os.environ['GRMPY'])

# project library
from   _randominit  import *

import grmpy


''' First, we check whether the function runs reliably. '''

for i in range(100):

    generateInitFile()

''' Second, we check whether the randomly generated file can be used to
simulate a datatest.'''


for i in range(100):

    generateInitFile()

    grmpy.simulate('test.grm.ini')


''' Third, let us see whether we can an run a single evaluation of the
likelihood function. This requires to add the feature that we can set
maxiter=0 in some way.'''



