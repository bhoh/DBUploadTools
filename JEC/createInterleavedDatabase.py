#! /usr/bin/env python
import os
import re
import sys
import subprocess
import argparse

#########################################################
# usage: python createInterleavedDatabase.py --era Summer16_03Feb2017All_V9_DATA --importDB Summer16_03Feb2017BCD_V9_DATA.db
#########################################################

parser = argparse.ArgumentParser()
parser.add_argument('--era', metavar='F', action='store', dest='era', help='Output era', required=True)
parser.add_argument('--importDB', metavar='DB', action='store', dest='db_import', help='starting database', required=True)
#parser.add_argument('--EndDB', metavar='DB', action='store', dest='db_end', help='Ending database', required=True)

options = parser.parse_args()

if not os.path.exists(options.db_import):
    raise argparse.ArgumentTypeError('importing database does not exist: %r' % options.db_import)

#if not os.path.exists(options.db_end):
#    raise argparse.ArgumentTypeError('25ns database does not exist: %r' % options.db_end)

jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype_AK4 = {'ak': [4]} #other options: ic, kt and any cone size
algsizetype_AK8 = {'ak': [8]} #other options: ic, kt and any cone size
jettype_base = ['pf', 'pfchs', 'puppi']
jettype_ext  = ['calo', 'jpt']
#jettype = ['pf', 'pfchs', 'puppi'] #other options: calo

ALGO_LIST_AK4_base = []
for k, v in algsizetype_AK4.iteritems():
    for s in v:
        for j in jettype_base:
	    ALGO_LIST_AK4_base.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi").replace("CALO","Calo")))
            #ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

ALGO_LIST_AK4_ext = []
for k, v in algsizetype_AK4.iteritems():
    for s in v:
        for j in jettype_ext:
	    ALGO_LIST_AK4_ext.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi").replace("CALO","Calo")))
            #ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

ALGO_LIST_AK8_base = []
for k, v in algsizetype_AK8.iteritems():
    for s in v:
        for j in jettype_base:
	    ALGO_LIST_AK8_base.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi").replace("CALO","Calo")))
            #ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

db_import= options.db_import
#db_end = options.db_end

##iov_list = [
##	("1", "252999",      db_start),
##	("253000", "254832", db_end),
##	("254833", "254833", db_start),
##	("254834", "254980", db_end),
##	("254981", "255031", db_start),
##	("255032", "",       db_end)
##]

iov_list = [
# 2017 ###
#	("1", "299329",       db_import) # B
#	("299337", "302029",       db_import) # C
#	("302030", "303434",       db_import) # D
#	("303435", "304826",       db_import) # E
	("304911", "306462",       db_import) # F
# 
# This is JEC internal definition, use this one instead of PPD definition
# 2016 ####
#	("1", "276811",       db_import) # BCD
#	("276831",	"278801",       db_import) # EF
#	("278802",	"280385",      db_import)  # G
#	("280919",	"",      db_import) # H
]

for aa in ALGO_LIST_AK4_base: #loop for jet algorithms
    for iov in iov_list:
        input_era = os.path.splitext(os.path.basename(iov[2]))[0]
        s1 = jec_type + '_' + input_era + '_' + aa
        s2 = jec_type + '_' + ERA + '_' + aa
        if not iov[1]:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]
        else:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]+" -e "+iov[1]
        print s
        subprocess.call(s.split())
for aa in ALGO_LIST_AK4_ext: #loop for jet algorithms
    for iov in iov_list:
        input_era = os.path.splitext(os.path.basename(iov[2]))[0]
        s1 = jec_type + '_' + input_era + '_' + aa
        s2 = jec_type + '_' + ERA + '_' + aa
        if not iov[1]:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]
        else:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]+" -e "+iov[1]
        print s
        subprocess.call(s.split())
for aa in ALGO_LIST_AK8_base: #loop for jet algorithms
    for iov in iov_list:
        input_era = os.path.splitext(os.path.basename(iov[2]))[0]
        s1 = jec_type + '_' + input_era + '_' + aa
        s2 = jec_type + '_' + ERA + '_' + aa
        if not iov[1]:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]
        else:
            s = "conddb_import -f sqlite_file:"+iov[2]+" -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]+" -e "+iov[1]
        print s
        subprocess.call(s.split())








'''
1-252999 50ns
253000-254832 25ns
254833-254833 50ns
254834-254980 25ns
254981-255031 50ns
255032-infinity 25ns

conddb_import -f sqlite_file:Summer15_50nsV5_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_50nsV5_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 1 -e 252999
conddb_import -f sqlite_file:Summer15_25nsV2_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_25nsV2_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 253000 -e 254832
conddb_import -f sqlite_file:Summer15_50nsV5_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_50nsV5_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 254833 -e 254833
conddb_import -f sqlite_file:Summer15_25nsV2_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_25nsV2_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 254834 -e 254980
conddb_import -f sqlite_file:Summer15_50nsV5_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_50nsV5_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 254981 -e 255031
conddb_import -f sqlite_file:Summer15_25nsV2_DATA.db -c sqlite_file:Summer15_V1_DATA.db -i JetCorrectorParametersCollection_Summer15_25nsV2_DATA_AK4PF -t JetCorrectorParametersCollection_Summer15_V1_DATA_AK4PF -b 255032 -e infinity

'''
