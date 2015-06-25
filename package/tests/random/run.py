#!/usr/bin/env python3
''' Script to start development test battery for the grmToolbox.
'''

# standard library
from datetime import timedelta
from datetime import datetime

import numpy as np

import argparse
import logging
import random
import sys

import grmpy.public as grmpy

# project library
from  grmpy.tests.random.modules._auxiliary import *
import grmpy.tests.random.modules._tests     as lib

# virtual environment


''' if not hasattr(sys, 'real_prefix'):
   raise AssertionError('Please use a virtual environment for testing')
'''

''' Main Function.
'''
def run(hours):
    ''' Run test battery.
    '''

    start, timeout = datetime.now(), timedelta(hours = hours)


    labels = ['A', 'B']

    # Initialize counter.
    dict_ = {}

    for label in labels:

        dict_[label] = {}

        dict_[label]['success'] = 0

        dict_[label]['failure'] = 0

    # Logging.
    logger = logging.getLogger('DEV-TEST')

    msg    = 'Initialization of a ' + str(hours) + ' hours testing run.'

    logger.info(msg)

    # Evaluation loop.
    while True:

        # Setup of test case.
        label = np.random.choice(labels)

        test  = getattr(lib,'test' + label)

        # Set seed.
        seed  = random.randrange(1, 100000)

        np.random.seed(seed)

        try:

            test()

            dict_[label]['success'] = dict_[label]['success'] + 1

        except:

            dict_[label]['failure'] = dict_[label]['failure'] + 1

            msg = 'Failure for test ' + label + ' with seed ' + str(seed)

            logger.info(msg)


        cleanup()

        # Timeout.
        current  = datetime.now()

        duration = current - start

        if(timeout < duration): break

    # Finishing.
    return dict_

''' Execution of module as script.
'''
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description =
      'Run development test battery of grmToolbox.',
      formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--hours', \
                        action  = 'store', \
                        dest    = 'hours', \
                        type    = float, \
                        default = 1.0, \
                        help    = 'run time in hours')

    hours = distributeInput(parser)

    startLogging()

    cleanup()

    dict_ = run(hours)

    finish(dict_, hours)
