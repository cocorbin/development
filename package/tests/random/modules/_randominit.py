''' Module that contains the functions for the random generation of an 
    initialization file.
'''

__all__ = ['generateInitFile', '_printDict', '_randomDict']


# standard library
import numpy as np

import shutil

''' Module-specific Parameters
'''
MAX_COEFFS   = 10
MAX_FACTORS  = 5
MAX_PERIODS  = 5
MAX_REPS     = 10
MAX_BOOT     = 20
MIN_AGENTS   = 10
MAX_AGENTS   = 1000
MAX_CPUS     = 4
MAX_DURATION = 5
MAX_ITER     = 10
MAX_MOMENTS  = 5

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

    if('hess' in dict_.keys()):
        
        hess = dict_['hess']
    
    else:
        
        hess = np.random.choice(['bfgs', 'numdiff'])

    if('AGENTS' in dict_.keys()):
    	
        AGENTS = dict_['AGENTS']
    
    else:
    	
        AGENTS = np.random.random_integers(1, 10000)

    
    ''' Overall
    '''    
    numBene     = np.random.random_integers(1, MAX_COEFFS)

    numCost     = np.random.random_integers(1, MAX_COEFFS)
    
    numCoeffs   = numBene + numCost
    
    positions   = list(range(1, numCoeffs + 4 + 3 + 2 + 1))

    numSim      = np.random.random_integers(MIN_AGENTS, MAX_AGENTS)
        
    numEst      = np.random.choice(list(range(MIN_AGENTS, numSim)) + ['None'])
    
    
    constraints = np.random.choice(['!', ' '], size = numCoeffs + 4 + 3 + 2 + 2).tolist()
    
    if(constraints.count(' ') == 0): constraints[-1] = ' '
    
    numFree = constraints.count(' ')
    
    
    dict_ = {}
    
    ''' DATA
    '''
    dict_['DATA'] = {}
    dict_['DATA']['source']  = 'test.dataset.dat'
    dict_['DATA']['agents']  = AGENTS
    dict_['DATA']['outcome']  = 0
    dict_['DATA']['treatment']  = np.random.random_integers(0,2)

    
    ''' BENEFITS and COSTS
    '''
    for flag in ['BENE', 'COST']:


        dict_[flag] = {}
        
        constr = constraints.pop()
        
        valBenefit = np.random.sample(2,)
        
        valCost = np.random.sample()
        
        if(flag == 'BENE'): dict_[flag]['int'] = [constr, valBenefit] 
        
        if(flag == 'COST'): dict_[flag]['int'] = [constr, valCost]
        
        if(flag == 'BENE'): dict_[flag]['sd'] = [constr, valBenefit] 
        
        if(flag == 'COST'): dict_[flag]['sd'] = [constr, valCost]
        
        count = numBene
        
        if(flag == 'COST'): count = numCost
        
        dict_[flag]['coeff'] = []

            
        for _ in range(count):

            pos, constr, truth  = positions.pop(), constraints.pop(), np.random.choice(['true', 'false'])           
            
            valBenefit = np.random.sample(2,)
            
            valCost = np.random.sample()
            
            if(flag == 'BENE'):dict_[flag]['coeff'] += [[pos, constr, valBenefit, truth]]
            
            if(flag == 'COST'): dict_[flag]['coeff'] += [[pos, constr, valCost]]


    ''' DIST
    '''
    dict_['DIST'] = {}
    
    dict_['DIST']['rho0'] = [constraints.pop(), np.random.uniform(-1.00, 1.00)]
            
    dict_['DIST']['rho1'] = [constraints.pop(), np.random.uniform(-1.00, 1.00)]
    
    
    ''' ESTIMATION
    '''

    dict_['ESTIMATION'] = {}
    dict_['ESTIMATION']['algorithm'] = optimizer
    dict_['ESTIMATION']['maxiter'] = np.random.random_integers(0, 10000)
    dict_['ESTIMATION']['start'] = starts
    dict_['ESTIMATION']['gtol'] = np.random.uniform(0, 1e-10)
    dict_['ESTIMATION']['epsilon'] = np.random.uniform(0.1, 10)
    dict_['ESTIMATION']['differences'] = differences
    
    for flag in ['marginal', 'conditional', 'average', 'asymptotics']:

        dict_['ESTIMATION'][flag] = np.random.choice(['true', 'false'])

    dict_['ESTIMATION']['hessian'] = hess
    dict_['ESTIMATION']['alpha'] = np.random.uniform(0.01, 0.05, 0.1)
    dict_['ESTIMATION']['simulations'] = np.random.random_integers(100,10000)
    dict_['ESTIMATION']['draws'] = np.random.random_integers(100,10000)

    
    ''' SIMULATION
    '''
    dict_['SIMULATION'] = {}
    
    dict_['SIMULATION']['agents']  = numSim

    dict_['SIMULATION']['seed']    = np.random.random_integers(1, 100)

    dict_['SIMULATION']['target']  = 'simulation.dat'
    
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
        if (flag == 'BENE'):

            str_ = ' {0:<6} {1:<15} {2} {3:<5} {4:<5} {5:<6} \n'

            file_.write(' ' + flag.upper() +'\n\n')

            ''' Coefficients.
            '''

            numCoeffs = len(dict_[flag]['coeff'])

            for i in range(numCoeffs):
                pos, constr, value1, value2, true = dict_[flag]['coeff'][i]


                file_.write(str_.format('coeff', pos, constr, value1, value2, true))
                file_.write('\n')

            ''' Intercept
            '''

            constr, value1, value2 = dict_[flag]['int']
            file_.write(str_.format('int', '', constr, value1, value2))
            file_.write('\n')
            
            ''' SD
            '''    
            
            constr, value1, value2 = dict_[flag]['sd']
            file_.write(str_.format('sd', '', constr, value1, value2))
            file_.write('\n')


        if (flag == 'COST'):

            numCoeffs = len(dict_[flag]['coeff'])

            for i in range(numCoeffs):
                pos, constr, value = dict_[flag]['coeff'][i]

                file_.write(str_.format('coeff', pos, constr, value))
                file_.write('\n')


            ''' Intercept
            '''

            constr, value = dict_[flag]['int']
            file_.write(str_.format('int', '', constr, value))
            file_.write('\n')
            
            ''' SD
            '''

            constr, value = dict_[flag]['sd']
            file_.write(str_.format('sd', '', constr, value))
            file_.write('\n')

        ''' SHOCKS
        '''
        str_ = ' {0:<5} {1}{2:<5}\n'

        file_.write(' ' + 'DIST' +'\n\n')

        for key_ in ['rho0', 'rho1']:

            constr, value = dict_['DIST'][key_]

            file_.write(str_.format(key_, constr, value))

    