import os

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing()

options.register('era',
        None,
        VarParsing.multiplicity.singleton,
        VarParsing.varType.string,
        'The era of the JER (ie, Summer15_25nsV2_MC)')

options.register('path',
        None,
        VarParsing.multiplicity.singleton,
        VarParsing.varType.string,
        'Where are located the txt files')

options.parseArguments()

if options.era is None:
    raise Exception("No era specified. Use the 'era' command line argument to set one.\n\tcmsRun <configuration> era=<era>")

if options.path is None:
    raise Exception("No path specified. Use the 'path' command line argument to set one.\n\tcmsRun <configuration> path=<era>")

jer_type    = 'JetResolutionObject'
ERA         = options.era
algsizetype = {'ak': [4, 8]} #other options: ic, kt and any cone size
#jettype = ['pf', 'pfchs', 'puppi'] #other options: calo
jettype = ['pf', 'pfchs'] #other options: calo

# Some sanity checks
if not '25ns' in ERA and not '50ns' in ERA:
    raise Exception('Invalid era: it must contains 25ns or 50ns')

if not 'data' in options.path:
    raise Exception('Invalid path: it must be a valid CMSSW data path')


ALGO_LIST = []
for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

output_db_file = '%s.db' % ERA

JER_SUFFIXES = ['DATAMCSF', 'MC_PtResolution']

import FWCore.ParameterSet.Config as cms 
process = cms.Process('jecdb') 
process.load('CondCore.DBCommon.CondDBCommon_cfi') 

process.CondDBCommon.connect = 'sqlite_file:%s' % output_db_file 

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1)) 
process.source = cms.Source('EmptySource') 

process.PoolDBOutputService = cms.Service('PoolDBOutputService', 
   process.CondDBCommon, 
   toPut = cms.VPSet( 
   ) 
) 

sequence = cms.Sequence()
for algo in ALGO_LIST:
    for suffix in JER_SUFFIXES:

        jer_file = os.path.join(options.path, '%s_%s_%s.txt' % (ERA, suffix, algo))
        print "Using %r as input for database" % jer_file

        process.PoolDBOutputService.toPut += [cms.PSet(
                record = cms.string('%s_%s' % (suffix, algo)), 
                tag    = cms.string('JER_%s_%s_%s' % (suffix, ERA, algo)), 
                label  = cms.string(algo)
                )]

        setattr(process, 'dbWriter%s%s' % (suffix, algo), cms.EDAnalyzer('JetResolutionDBWriter',
            record = cms.untracked.string("%s_%s" % (suffix, algo)),
            file   = cms.untracked.FileInPath(jer_file)
            )
            )

        sequence += getattr(process, 'dbWriter%s%s' % (suffix, algo))


process.p = cms.Path(sequence)
