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

parser.add_option('--prompt', metavar='F', action='store_true',
                  dest='prompt',
                  help='Upload to prompt')

parser.add_option('--offline', metavar='F', action='store_true',
                  dest='offline',
                  help='Upload to offline')

parser.add_option('--since', metavar='N', action='store', type=int,
                  dest='since',
                  help='Since IOV')

(options, args) = parser.parse_args()

if not options.prompt and not options.offline:
    raise Exception("You need to specify either --prompt or --offline")

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
p3 = re.compile(r'SYNC')
p4 = re.compile(r'SINCE')

#******************   definitions  **********************************
jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetype = {'ak':[4,8]} #other options: ic, kt and any cone size
jettype = ['pf','pfchs', 'puppi'] #other options: calo

ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))
#*********************************************************************

files = []


### L2+L3 Corrections
for aa in ALGO_LIST: #loop for jet algorithms

    s1 = "JetCorrectorParametersCollection_%s_v0_express" % aa if options.prompt else jec_type + '_' + ERA + '_' + aa
    s2 = jec_type + '_' + ERA + '_' + aa
    s3 = "express" if options.prompt else "offline"
    s4 = str(options.since) if options.since else "null"
    k1 = p1.sub( s1, fileContents )
    k2 = p2.sub( s2, k1 )
    k3 = p3.sub( s3, k2 )
    k4 = p4.sub( s4, k3 )
    k2outfile = s1 + '.txt'
    print '--------------------------------------'
    print 'ORCOFF File for jet correction : ' + s1
    print 'Written to ' + k2outfile
    FILE = open(k2outfile,"w")
    FILE.write(k4)       
    files.append( k2outfile )
    


for ifile in files :
    if options.prep :
        append = '_test'
    else :
         append = ''
    s = "./dropBoxOffline" + append + ".sh "+options.sqlite_file+" " + ifile
    print s
    subprocess.call( ["./dropBoxOffline" + append + ".sh", options.sqlite_file, ifile])

