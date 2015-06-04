''' This modules contains the tests for the continuous integration efforts.
'''

__runtest__ = ['test A']

# standard library
import numpy    as np

import sys
import os

# project library
import _auxiliary
import _randominit

# grmToolbox
# sys.path.insert(0, os.environ['GRM_TOOLBOX'])


from scripts.simulate                import simulate
from scripts.estimate                import estimate
from scripts.perturb                 import perturb

from tools.auxiliary                 import readStep

''' Main
'''

def testA():
    ''' Testing if a random estimation task can be handled without any problem
        for one step.
    '''
    # Constraints.
    _randomInit.generateInitFile()

    # Simulate dataset.
    simulate()

    # Create estimation task.
    scale = np.random.uniform(-0.05, 0.05)

    perturb(scale = scale, seed = 123)

    # Execute on task.
    estimate(resume = True, useSimulation = True)


