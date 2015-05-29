#!/usr/bin/env python
"""  Module that contains testing of complete estimation runs. The purpose
    is to detect immediately if there are any changes in the estimation 
    output. This allows to check if the change was intended to occur. 
    The success of the tests depends heavily on the software versions and
    system architecture. They are not expected to success on other machines 
    other than @heracles.

"""
# standard library
import cPickle as pkl
import os
import sys

from nose.core import *
from nose.tools import *

# Pythonpath
sys.path.insert(0, os.environ['GRM_TOOLBOX'])

# project library
import grmToolbox

''' Test class '''

class TestEstimationRuns(object):
    """ Testing full estimation runs for a variety of data specifications.
    """
    @staticmethod
    def test_est_run_one():
        """ Basic estimation run, One.
        """
        # Run command
        init_file = 'dat/testInit_A.ini'
        
        grmToolbox.estimate(init_file, resume=False, useSimulation=False)

        # Assessment of results
        rslt_dict = pkl.load(open('rslt.grm.pkl', 'r'))
        
        max_rslt = rslt_dict['maxRslt']
        
        # Assertions
        assert_almost_equal(max_rslt['fun'], 1.643038068973831)

        # Cleanup
        grmToolbox.cleanup(resume=False)

    @staticmethod
    def test_est_run_two():
        """ Basic estimation run, Two.
        """
        # Run command.
        init_file = 'dat/testInit_B.ini'
        
        grmToolbox.estimate(init_file, resume=False, useSimulation=False)

        # Assessment of results.
        rslt_dict = pkl.load(open('rslt.grm.pkl', 'r'))

        # Assertions.
        assert_almost_equal(rslt_dict['maxRslt']['fun'], 1.6569859824560313)

        # Cleanup.
        grmToolbox.cleanup(resume=False)

    @staticmethod
    def test_est_run_three():
        """ Basic estimation run, Three.
        """
        # Run command
        init_file = 'dat/testInit_C.ini'
        
        grmToolbox.estimate(init_file, resume = False, useSimulation = False)

        # Assessment of results
        rslt_dict = pkl.load(open('rslt.grm.pkl', 'r'))

        # Assertions
        assert_almost_equal(rslt_dict['maxRslt']['fun'], 1.6281817748415393)

        assert_almost_equal(rslt_dict['bmteExPost']['estimate'][50],
        -0.10666298513882175)
        assert_almost_equal(rslt_dict['bmteExPost']['confi']['upper'][50],
        -0.078545042872650739)
        assert_almost_equal(rslt_dict['bmteExPost']['confi']['lower'][50],
        -0.13429949460194246)
   
        assert_almost_equal(rslt_dict['smteExAnte']['estimate'][50],
        -0.13443440314930999)
        assert_almost_equal(rslt_dict['smteExAnte']['confi']['upper'][50],
        -0.10163853993013783)
        assert_almost_equal(rslt_dict['smteExAnte']['confi']['lower'][50],
        -0.16935220247013208)
   
        #Assert relationship between parameters
        for i in range(99):
            
            cmteExAnte = rslt_dict['cmteExAnte']['estimate'][i]
            smteExAnte = rslt_dict['smteExAnte']['estimate'][i]
            bmteExPost = rslt_dict['bmteExPost']['estimate'][i]
            
            assert_almost_equal(smteExAnte, bmteExPost - cmteExAnte)
   
        # Cleanup.
        grmToolbox.cleanup(resume=False)

    @staticmethod
    def test_est_run_four():
        """ Basic estimation run, Four.
        """
        # Run command
        initFile = 'dat/testInit_D.ini'

        grmToolbox.estimate(initFile, resume=False, useSimulation=False)

        # Assessment of results.
        rslt_dict = pkl.load(open('rslt.grm.pkl', 'r'))

        # Assertions.
        assert_almost_equal(rslt_dict['bteExPost']['average']['estimate'],
        -0.14337500688760152)
        assert_almost_equal(rslt_dict['bteExPost']['treated']['estimate'],
        0.06553651561690533)
        assert_almost_equal(rslt_dict['bteExPost']['untreated']['estimate'],
        -0.30751977456971408)

        assert_almost_equal(rslt_dict['bteExAnte']['average']['estimate'],
        -0.14337500688760152)
        assert_almost_equal(rslt_dict['bteExAnte']['treated']['estimate'],
        0.06553651561690533)
        assert_almost_equal(rslt_dict['bteExAnte']['untreated']['estimate'],
        -0.30751977456971408)

        assert_almost_equal(rslt_dict['cte']['average']['estimate'],
        0.0786721631745564)
        assert_almost_equal(rslt_dict['cte']['treated']['estimate'],
        -0.7216392651098148)
        assert_almost_equal(rslt_dict['cte']['untreated']['estimate'],
        0.7074882853979908)

        assert_almost_equal(rslt_dict['ste']['average']['estimate'],
        -0.2220471700621577)
        assert_almost_equal(rslt_dict['ste']['treated']['estimate'],
        0.7871757807267197)
        assert_almost_equal(rslt_dict['ste']['untreated']['estimate'],
        -1.0150080599677049)

        # Cleanup.
        grmToolbox.cleanup(resume = False)

if __name__ == '__main__': 
    
    runmodule()   
