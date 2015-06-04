#!/usr/bin/env python

""" Module that contains the functions for the random generation of an
    initialization file.
"""

__all__ = ['generateInitFile', '_printDict', '_randomDict']


# standard library
import numpy as np

import shutil

''' Module-specific Parameters
'''
MAX_COEFFS   = 10
MAX_FACTORS  = 5
MAX_TREAT    = 2
MIN_TREAT    = 0
MAX_DRAWS    = 10000
MIN_DRAWS    = 10
MAX_SIMS     = 10000
MIN_SIMS     = 10
MIN_AGENTS   = 'None'
MAX_AGENTS   = 10000
MIN_ITER     = 'None'
MAX_ITER     = 10000

''' Public Function
'''
def generateInitFile(dict_ = {}):
    ''' Get a random initialization file.
    '''
    # Antibugging.
    assert (isinstance(dict_, dict))

    dict_ = _randomDict(dict_)

    _printDict(dict_)

    # Finishing.
    return dict_

''' Private Functions
'''
def _randomDict(dict_  = {}):
    ''' Draw random dictionary instance that can be processed into an
        initialization file.
    '''
        # Antibugging.
    assert ((dict_ is None) or (isinstance(dict_, dict)))

    if('optimizer' in dict_.keys()):

        optimizer = dict_['optimizer']
    else:
        optimizer = np.random.choice(['bfgs', 'powell'])

    if('truth' in dict_.keys()):
         truth = dict_['truth']
    else:
         truth = np.random.choice(['true', 'false'])
    if('differences' in dict_.keys()):
        differences = dict_['differencess']
    else:
        differences = np.random.choice(['one-sided', 'two-sided'])
    if('starts' in dict_.keys()):
        starts = dict_['starts']
    else:
        starts = np.random.choice(['manual', 'auto'])

    if('hessian' in dict_.keys()):
        hessian = dict_['hessian']
    else:
        hess = np.random.choice(['bfgs', 'numdiff'])
        
    if('AGENTS' in dict_.keys()):
    	AGENTS = dict_['AGENTS']
    else:
    	AGENTS = np.random.choice('None', np.random.random_integers(1, 10000))	    



    ''' Overall
    '''
    numBene     = np.random.random_integers(0, MAX_COEFFS)
    numCost     = np.random.random_integers(0, MAX_COEFFS)
    numCoeffs   = numBene + numCost
    positions   = list(range(1, numCoeffs + 4 + 3 + 2 + 1))
    numSim      = np.random.random_integers(MIN_SIMS, MAX_SIMS)

    constraints = np.random.choice(['!', ' '], size = numCoeffs + 4 + 3 + 2 + 2).tolist()

    if(constraints.count(' ') == 0): constraints[-1] = ' '
    numFree = constraints.count(' ')


    dict_ = {}

# !! NEED TO CONSTRUCT TEST DATA SET !!

    ''' DATA
    '''
    dict_['DATA'] = {}
    dict_['DATA']['source']  = 'test.dataset.dat'
    dict_['DATA']['agents']  = AGENTS
    dict_['DATA']['outcome']  = 0
    dict_['DATA']['treatment']  = np.random.random_integers(0,2)


    ''' BENEFITS and COST
    '''
    for flag in ['BENE', 'COST']:

        dict_[flag] = {}

        constr, val1, val2 = constraints.pop(), np.random.sample(), np.random.sample()
        val3, val4, val5, val6 = np.random.sample(), np.random.rand(0,5), np.random.rand(0,5), np.random.rand(0,5)
        if(flag == 'BENE'):
            dict_[flag]['int'] = [constr, val1, val2]
            dict_[flag]['sd'] = [constr, val4, val5]
        
        if(flag == 'COST'):
            dict_[flag]['sd'] = [constr, val6]
            dict_[flag]['int'] = [constr, val3]

        
        count = numBene
        if(flag == 'COST'): count = numCost

        dict_[flag]['coeff'] = []

        for _ in range(count):
            pos, constr, truth  = positions.pop(), constraints.pop(), np.random.choice(['true', 'false'])
            val1, val2 = np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)
            val3 = np.random.uniform(-1.0, 1.0)
            if(flag == 'BENE'):
                pos, constr, truth  = positions.pop(), constraints.pop(), np.random.choice(['true', 'false'])
                val1, val2 = np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)
                dict_[flag]['coeff'] += [pos, constr, val1, val2, truth]
            if(flag == 'COST'):
                val3 = np.random.uniform(-1.0, 1.0)
                dict_[flag]['coeff'] += [pos, constr, val3]


    ''' DIST
    '''
    dict_['DIST'] = {}
    dict_['DIST']['rho0'] = [constraints.pop(), np.random.uniform(-1.0, 1.0)]
    dict_['DIST']['rho1'] = [constraints.pop(), np.random.uniform(-1.0, 1.0)]

#  !! SHOULD 'ALGORITHM' BE REPLACED BY EXTERNAL optimizers.ini?  !!

    ''' ESTIMATION
    '''
    dict_['ESTIMATION'] = {}
    dict_['ESTIMATION']['algorithm'] = optimizer
    dict_['ESTIMATION']['maxiter'] = np.random.random_integers(0, 10000)
    dict_['ESTIMATION']['start'] = starts
    dict_['ESTIMATION']['gtol'] = [constraints.pop(), np.random.uniform(0, 1e-10)]
    dict_['ESTIMATION']['epsilon'] = np.random.uniform(0.1, 10)
    dict_['ESTIMATION']['differences'] = differences
    dict_['ESTIMATION']['marginal'] = truth
    dict_['ESTIMATION']['conditional'] = truth
    dict_['ESTIMATION']['average'] = truth
    dict_['ESTIMATION']['asymptotics'] = truth
    dict_['ESTIMATION']['hessian'] = hess
    dict_['ESTIMATION']['alpha'] = np.random.choice(0.01, 0.05, 0.1)
    dict_['ESTIMATION']['simulations'] = np.random.random_integers(100,10000)
    dict_['ESTIMATION']['draws'] = np.random.random_integers(100,10000)


    ''' SIMULATION
    '''
    dict_['SIMULATION'] = {}
    dict_['SIMULATION']['agents']  = AGENTS
    dict_['SIMULATION']['seed']    = np.random.random_integers(1, 1000)
    dict_['SIMULATION']['target'] = 'test.simulation.dat'

    # Finishing.
    return dict_

def _printDict(dict_):
    ''' Generate a random initialization file.
    '''
    # Antibugging.
    assert (isinstance(dict_, dict))

    # Create initialization.
    with open('test.grm.ini', 'w') as file_:

        ''' DATA, BENEFITS, COST, ESTIMATION, and SIMULATION
        '''
        for flag in dict_.keys():

            if(flag in ['DIST', 'BENE', 'COST']): continue

            str_ = ' {0:<15} {1:<15} \n'

            file_.write(' ' + flag.upper() +'\n\n')

            for keys_ in dict_[flag]:

                file_.write(str_.format(keys_, dict_[flag][keys_]))

            file_.write('\n')

        ''' BENE and COST
        '''
        for flag in ['BENE', 'COST']:

            str_ = ' {0:<6} {1:<15} {2} {3:<5} {4:<5} {5:<6} \n'

            file_.write(' ' + flag.upper() +'\n\n')

            ''' Coefficients.
            '''

            if flag in ['BENE']:
                numCoeffs = len(dict_[flag]['coeff'])

                for i in range(numCoeffs):
                    pos, constr, value1, value2, true = dict_[flag]['coeff'][i]

                    file_.write(str_.format('coeff', pos, constr, value1, value2, true))
                    file_.write('\n')

            if flag in ['COST']:
                numCoeffs = len(dict_[flag]['coeff'])
                for i in range(numCoeffs):
                    pos, constr, value = dict_[flag]['coeff'][i]

                    file_.write(str_.format('coeff', pos, constr, value))
                    file_.write('\n')


            ''' Intercept
            '''
            if flag in ['BENE']:
                constr, value1, value2 = dict_[flag]['int']
                file_.write(str_.format('int', '', constr, value1, value2))
                file_.write('\n')

            if flag in ['COST']:
                constr, value = dict_[flag]['int']
                file_.write(str_.format('int', '', constr, value))
                file_.write('\n')

        ''' SHOCKS
        '''
        str_ = ' {0:<5} {1}{2:<5}\n'

        file_.write(' ' + 'DIST' +'\n\n')

        for key_ in ['rho0', 'rho1']:

            constr, value = dict_['DIST'][key_]

            file_.write(str_.format(key_, constr, value))
