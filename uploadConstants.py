#! /usr/bin/env python
import os
import re
import sys
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--sqlite_file', metavar='F', type='string', action='store',
                  dest='sqlite_file',
                  help='Input sqlite file')

parser.add_option('--era', metavar='F', type='string', action='store',
                  dest='era',
                  help='Input era')
parser.add_option('--prep', metavar='F', action='store_true',
                  dest='prep',
                  help='Upload to prep area')
(options, args) = parser.parse_args()

#******************   template file  **********************************
if options.prep :
    templateFile = open('templateForDropbox_PREP.txt', 'r')
else :
    templateFile = open('templateForDropbox_PRODUCTION.txt', 'r')
fileContents = templateFile.read(-1)
print '--------------- TEMPLATE :  -----------------'
print fileContents
p1 = re.compile(r'TAGNAME')
p2 = re.compile(r'PRODNAME')
p3 = re.compile(r'ALGNAME')
#******************   definitions  **********************************
jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype = {'ak':[4,8]} #other options: ic, kt and any cone size
jettype = ['pf','pfchs','puppi'] #other options: calo

ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))
#*********************************************************************

files = []


### L2+L3 Corrections
for aa in ALGO_LIST: #loop for jet algorithms

    s1 = jec_type + '_' + ERA + '_' + aa
    s2 = jec_type + '_' + ERA + '_' + aa
    s3 = aa
    k1 = p1.sub( s1, fileContents )
    k2 = p2.sub( s2, k1 )
    k3 = p3.sub( s3, k2 )
    k2outfile = s2 + '.txt'
    print '--------------------------------------'
    print 'ORCOFF File for jet correction : ' + s2
    print 'Written to ' + k2outfile
    FILE = open(k2outfile,"w")
    FILE.write(k3)       
    files.append( k2outfile )
    


for ifile in files :
    if options.prep :
        append = '_test'
    else :
         append = ''
    s = "./dropBoxOffline" + append + ".sh "+options.sqlite_file+" " + ifile
    print s
    subprocess.call( ["./dropBoxOffline" + append + ".sh", options.sqlite_file, ifile])

