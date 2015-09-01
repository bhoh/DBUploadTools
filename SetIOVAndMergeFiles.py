#! /usr/bin/env python
import os
import re
import sys
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--era', metavar='F', type='string', action='store',
                  dest='era',
                  help='Input era')
(options, args) = parser.parse_args()


jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype = {'ak':[4,8]} #other options: ic, kt and any cone size
jettype = ['pf','pfchs','puppi'] #other options: calo

ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

iov_list = [
	("1","252999","Summer15_50nsV5_DATA"),
	("253000","254832","Summer15_25nsV2_DATA"),
	("254833","254833","Summer15_50nsV5_DATA"),
	("254834","254980","Summer15_25nsV2_DATA"),
	("254981","255031","Summer15_50nsV5_DATA"),
	("255032","","Summer15_25nsV2_DATA")
]

for aa in ALGO_LIST: #loop for jet algorithms
	for iov in iov_list:
		s1 = jec_type + '_' + iov[2] + '_' + aa
		s2 = jec_type + '_' + ERA + '_' + aa
		if not iov[1]:
			s = "conddb_import -f sqlite_file:"+iov[2]+".db -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]
		else:
			s = "conddb_import -f sqlite_file:"+iov[2]+".db -c sqlite_file:"+ERA+".db -i "+s1+" -t "+s2+" -b "+iov[0]+" -e "+iov[1]
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