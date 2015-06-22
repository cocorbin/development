''' Module that contains the functions for the random generation of an 
    initialization file.
'''

__all__ = ['generateInitFile', '_printDict', '_randomDict']


# standard library
import numpy as np



''' Module-specific Parameters
'''
MAX_COEFFS   = 10
MIN_AGENTS   = 10
MAX_AGENTS   = 1000

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
    dict_['DATA']['treatment']  = 1

    
    ''' BENEFITS and COSTS
    '''
    for flag in ['BENE', 'COST']:


        dict_[flag] = {}
        
        constr = constraints.pop()
        
        valBene1, valBene2 = round(np.random.ranf(),2), round(np.random.ranf(),2)
        valBene3, valBene4 = round(np.random.ranf(),2), round(np.random.ranf(),2)
        
        valCost1 = round(np.random.ranf(),2)
        valCost2 = round(np.random.ranf(),2)
        
        if(flag == 'BENE'): dict_[flag]['int'] = [constr, valBene1, valBene2] 
        
        if(flag == 'COST'): dict_[flag]['int'] = [constr, valCost1]
        
        if(flag == 'BENE'): dict_[flag]['sd'] = [constr, valBene3, valBene4] 
        
        if(flag == 'COST'): dict_[flag]['sd'] = [constr, valCost2]
        
        count = numBene
        
        if(flag == 'COST'): count = numCost
        
        dict_[flag]['coeff'] = []

            
        for _ in range(count):

            pos, constr, truth  = positions.pop(), constraints.pop(), np.random.choice(['true', 'false'])           
            
            valBene1, valBene2 = round(np.random.ranf(),2), round(np.random.ranf(),2)
            
            valCost = round(np.random.ranf(),2)
            
            if(flag == 'BENE'):dict_[flag]['coeff'] += [[pos, constr, valBene1, valBene2, truth]]
            
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

    if(dict_['ESTIMATION']['algorithm'] == 'powell'): dict_['ESTIMATION']['hessian'] = 'bfgs'

    dict_['ESTIMATION']['alpha'] = np.random.choice([0.01, 0.05, 0.1])
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
    
        ''' DATA
        '''
        
        str_ = ' {0:<15} {1:<15} \n'

        file_.write('DATA' +'\n')

        for keys_ in ['source', 'agents']:

            file_.write(str_.format('   '+ keys_, dict_['DATA'][keys_]))
        
        file_.write('\n')
            
        for keys_ in ['outcome', 'treatment']:

            file_.write(str_.format('   '+ keys_, dict_['DATA'][keys_]))

        file_.write('\n')
        
        ''' BENE
        '''
        
        str_ = ' {0:<8} {1:<5} {2}{3:<3} {4}{5:<3} {6:<6} \n'

        file_.write('BENE' +'\n\n')     
        
                
        ''' BENE: Coefficients
        '''
        
        numCoeffs = len(dict_['BENE']['coeff'])

        for i in range(numCoeffs):
            
            pos, constr, val1, val2, true = dict_['BENE']['coeff'][i]

            file_.write(str_.format('   ' + 'coeff', pos, constr, val2, constr, val2, true))

        file_.write('\n')

        ''' BENEFITS: Intercept & SD
        '''
        str_ = ' {0:<8} {1:<5} {2}{3:<5} {4}{5:<5} \n'
        
        for key_ in ['int', 'sd']:
        
            constr, val1, val2 = dict_['BENE'][key_]
            file_.write(str_.format('   ' + key_, ' ',constr, val1, constr, val2))
        
        file_.write('\n')

        ''' COST
        '''
        
        str_ = ' {0:<8} {1:<5} {2}{3:<5} \n'
        file_.write('COST' +'\n\n')

        numCoeffs = len(dict_['COST']['coeff'])

        for i in range(numCoeffs):
            
            pos, constr, value = dict_['COST']['coeff'][i]

            file_.write(str_.format('   ' + 'coeff', pos, constr, value))
            
        file_.write('\n')


        ''' COST: Intercept & SD
        '''
        
        for key_ in ['int', 'sd']:
        
            constr, value = dict_['COST'][key_]
            
            file_.write(str_.format('   ' + key_, ' ', constr, value))
        
        file_.write('\n')



        ''' DIST
        '''
        
        str_ = ' {0:<5} {1}{2:<5} \n'

        file_.write('DIST' +'\n\n')

        for key_ in ['rho0', 'rho1']:

            constr, value = dict_['DIST'][key_]

            file_.write(str_.format('   ' + key_, constr, value))
        
        file_.write('\n')
        
        
        '''ESTIMATION
        '''
        
        str_ = ' {0:<15} {1:<15} \n'

        file_.write('ESTIMATION' +'\n\n')
        
        for key_ in ['algorithm', 'maxiter', 'start', 'gtol']:
        
            file_.write(str_.format('   ' + key_, dict_['ESTIMATION'][key_]))
            
        file_.write('\n')
        
        for key_ in ['epsilon', 'differences']:
        
            file_.write(str_.format('   ' + key_, dict_['ESTIMATION'][key_]))
        
        file_.write('\n')
        
        for key_ in ['marginal', 'conditional', 'average']:
        
            file_.write(str_.format('   ' + key_, dict_['ESTIMATION'][key_]))
            
        file_.write('\n')
        
        for key_ in ['asymptotics', 'hessian']:
        
            file_.write(str_.format('   ' + key_, dict_['ESTIMATION'][key_]))
        
        file_.write('\n')
        
        for key_ in ['draws', 'simulations', 'alpha']:
        
            file_.write(str_.format('   ' + key_, dict_['ESTIMATION'][key_]))

        file_.write('\n')
        
        ''' SIMULATION
        '''
        
        str_ = ' {0:<15} {1:<15} \n'

        file_.write('SIMULATION' +'\n\n')

        for keys_ in ['agents', 'seed', 'target']:

            file_.write(str_.format('   ' + keys_, dict_['SIMULATION'][keys_]))
