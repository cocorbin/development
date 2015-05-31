''' This modules contains the tests for the continuous integration efforts.
'''

__all__ = ['testA', 'testB']

# standard library
import numpy    as np

import sys
import os

# project library
import _auxiliary
import _randominit

# structToolbox
sys.path.insert(0, os.environ['GRMPY'])


from scripts.simulate                import simulate
from scripts.estimate                import estimate
from scripts.perturb                 import perturb

from tools.auxiliary                 import readStep

''' Main
'''
def testA():
    ''' Testing if a the evaluation results are the same regardless if the
        toolbox was compiled either normal or fast.
    '''
    # Constraints.
    _randominit.generateInitFile()

    # Simulation.
    simulate()

    # Perturb
    fval, scale = None, np.random.uniform(-0.5, 0.5)

    perturb(scale = scale, seed = 123)

    # Evaluation of function


    _auxiliary.compileToolbox()

    # Estimate
    estimate(useSimulaton = True)

    # Evaluate success.
    rslt = readStep('fval')

    if(fval is None): fval = rslt

    err = (np.allclose(rslt, fval) != True)

    assert (err == False)


def testB():
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


