#!/usr/bin/env python

import subprocess

era = 'Summer15_V1_DATA'

iovs = [
    #'JetCorrectorParametersCollection_'+era+'_AK5Calo',
    #'JetCorrectorParametersCollection_'+era+'_AK5JPT',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_AK5TRK',
    #'JetCorrectorParametersCollection_'+era+'_AK7Calo',
    #'JetCorrectorParametersCollection_'+era+'_AK7JPT',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_KT4Calo',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_KT4PF',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_KT6Calo',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_KT6PF',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_IC5Calo',
    #'JetCorrectorParametersCollection_Summer13_V1_MC_IC5PF',
    #'JetCorrectorParametersCollection_'+era+'_AK1PF',
    #'JetCorrectorParametersCollection_'+era+'_AK2PF',
    #'JetCorrectorParametersCollection_'+era+'_AK3PF',
    'JetCorrectorParametersCollection_'+era+'_AK4PF',
    #'JetCorrectorParametersCollection_'+era+'_AK5PF',
    #'JetCorrectorParametersCollection_'+era+'_AK6PF',
    #'JetCorrectorParametersCollection_'+era+'_AK7PF',
    'JetCorrectorParametersCollection_'+era+'_AK8PF',
    #'JetCorrectorParametersCollection_'+era+'_AK9PF',
    #'JetCorrectorParametersCollection_'+era+'_AK10PF',
    #'JetCorrectorParametersCollection_'+era+'_AK1PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK2PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK3PFchs',
    'JetCorrectorParametersCollection_'+era+'_AK4PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK5PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK6PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK7PFchs',
    'JetCorrectorParametersCollection_'+era+'_AK8PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK9PFchs',
    #'JetCorrectorParametersCollection_'+era+'_AK10PFchs',
    'JetCorrectorParametersCollection_'+era+'_AK4PFPuppi',
    'JetCorrectorParametersCollection_'+era+'_AK8PFPuppi'
    ]

for iov in iovs :
    #s = 'cmscond_list_iov -c sqlite_file:'+era+'.db -t ' + iov
    s = 'conddb --db '+era+'.db list ' + iov
    subprocess.call( [s, ""], shell=True )    
