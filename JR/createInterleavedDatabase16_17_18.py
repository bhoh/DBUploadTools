#! /usr/bin/env python
import os
import re
import sys
import subprocess
import argparse

#########################################################
# usage: python createInterleavedDatabase16_17.py --era Summer16_03Feb2017All_V9_DATA --importDB Summer16_03Feb2017BCD_V9_DATA.db
#########################################################

parser = argparse.ArgumentParser()
parser.add_argument('--era', metavar='F', action='store', dest='era', help='Output era', required=True)
parser.add_argument('--importDB', nargs='+', metavar='DB', action='store', dest='db_import', help='starting database', required=True)
#parser.add_argument('--EndDB', metavar='DB', action='store', dest='db_end', help='Ending database', required=True)

options = parser.parse_args()
'''
if not os.path.exists(options.db_import):
    raise argparse.ArgumentTypeError('importing database does not exist: %r' % options.db_import)
'''
#if not os.path.exists(options.db_end):
#    raise argparse.ArgumentTypeError('25ns database does not exist: %r' % options.db_end)

jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype = {'ak': [4, 8]} #other options: ic, kt and any cone size
jettype = ['pf', 'pfchs', 'puppi'] #other options: calo

ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

JR_SUFFIXES = ['SF', 'PtResolution', 'PhiResolution', 'EtaResolution']

db_import= options.db_import
#db_end = options.db_end

iov_list=[]
for db in db_import:
    if not os.path.exists(db):
        raise RuntimeError('%s is not exist'%db)
    errorFlag = False
    if re.search(r'^[A-Z][a-z]*16_', db):
            iov_list.append(("1", "294644", db))
    elif re.search(r'^[A-Z][a-z]*17_', db):
            iov_list.append(("294645", "307082", db))
    elif re.search(r'^[A-Z][a-z]*18_', db):
        if re.search(r'18_V[0-9]*', db):
            iov_list.append(("307083", "", db))
        elif re.search(r'ABC_V[0-9]*', db):
            iov_list.append(("307083", "320393", db))
        elif re.search(r'D_V[0-9]*', db):
            iov_list.append(("320394", "", db))
        else:
            errorFlag=True
    else:
        errorFlag=True

    if errorFlag:
        raise RuntimeError('an error occurred during the setting run range of %s'%db)

##iov_list = [
##	("1", "252999",      db_start),
##	("253000", "254832", db_end),
##	("254833", "254833", db_start),
##	("254834", "254980", db_end),
##	("254981", "255031", db_start),
##	("255032", "",       db_end)
##]
'''
iov_list = [
# 2017 ###
# 	("1", "299329",       db_import) # B
# 	("297020", "299329",       db_import) # B
# 	("299337", "302029",       db_import) # C
# 	("302030", "303434",       db_import) # D
# 	("302030", "304826",       db_import) # DE
# 	("303435", "304826",       db_import) # E
####	("304911", "306462",       db_import) # F
 	("304911", "",       db_import) # F
# 
# This is JEC internal definition, use this one instead of PPD definition
# 2016 ####
#	("1", "276811",       db_import) # BCD
#	("276831",	"278801",       db_import) # EF
#	("278802",	"280385",      db_import)  # G
#	("280919",	"",      db_import) # H
# 2016 V9, 10, 11 ####
# 	("1", "276811",       db_import) # BCD
#	("276831",	"278801",       db_import) # EF early F
#	("278802",	"297019",      db_import)  # earlyF GH use this to combine with 2017
####	("278802",	"284044",      db_import)  # earlyF GH
]
'''


for algo in ALGO_LIST:
    for suffix in JR_SUFFIXES:
        for iov in iov_list:
            input_era = os.path.splitext(os.path.basename(iov[2]))[0]
            s1 = "_".join(["JR", input_era, suffix, algo])
            s2 = "_".join(["JR", ERA, suffix, algo])
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
