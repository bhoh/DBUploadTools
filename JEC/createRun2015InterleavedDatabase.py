#! /usr/bin/env python
import os
import re
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--era', metavar='F', action='store', dest='era', help='Output era', required=True)
parser.add_argument('--50ns', metavar='DB', action='store', dest='db_50ns', help='50ns database', required=True)
parser.add_argument('--25ns', metavar='DB', action='store', dest='db_25ns', help='25ns database', required=True)

options = parser.parse_args()

if not os.path.exists(options.db_50ns):
    raise argparse.ArgumentTypeError('50ns database does not exist: %r' % options.db_50ns)

if not os.path.exists(options.db_25ns):
    raise argparse.ArgumentTypeError('25ns database does not exist: %r' % options.db_25ns)

jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype = {'ak': [4,8]} #other options: ic, kt and any cone size
jettype = ['pf', 'pfchs', 'puppi'] #other options: calo

ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

db_50ns = options.db_50ns
db_25ns = options.db_25ns

iov_list = [
	("1", "252999",      db_50ns),
	("253000", "254832", db_25ns),
	("254833", "254833", db_50ns),
	("254834", "254980", db_25ns),
	("254981", "255031", db_50ns),
	("255032", "",       db_25ns)
]

for aa in ALGO_LIST: #loop for jet algorithms
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
