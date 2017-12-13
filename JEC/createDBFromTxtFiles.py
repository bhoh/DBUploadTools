from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing()

options.register('era',
        None,
        VarParsing.multiplicity.singleton,
        VarParsing.varType.string,
        'The era of the JEC (ie, Summer15_25nsV2_MC)')

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

jec_type    = 'JetCorrectorParametersCollection'
ERA         = options.era
algsizetypeAK4 = {'ak': [4]} #other options: ic, kt and any cone size
algsizetypeAK8 = {'ak': [8]} #other options: ic, kt and any cone size
#jettypeAK4 = ['pf', 'pfchs', 'puppi']# for Summer16_V1_MC 
jettypeAK4 = ['pf', 'pfchs', 'puppi', 'calo', 'jpt'] 
jettypeAK8 = ['pf', 'pfchs', 'puppi'] 
#jettype = ['pf', 'pfchs', 'puppi'] #other options: calo

# Some sanity checks
#if not '25ns' in ERA and not '50ns' in ERA:
#    raise Exception('Invalid era: it must contains 25ns or 50ns')

if not 'DATA' in ERA and not 'MC' in ERA:
    raise Exception('Invalid era: it must contains DATA or MC')

if not 'data' in options.path:
    raise Exception('Invalid path: it must be a valid CMSSW data path')


ALGO_LIST = []
for k, v in algsizetypeAK4.iteritems():
    for s in v:
        for j in jettypeAK4:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi").replace("CALO","Calo")))
for k, v in algsizetypeAK8.iteritems():
    for s in v:
        for j in jettypeAK8:
            ALGO_LIST.append(str(k.upper()+str(s)+j.upper().replace("CHS","chs").replace("PUPPI","PFPuppi")))

output_db_file = '%s.db' % ERA

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
    process.PoolDBOutputService.toPut += [cms.PSet(
            record = cms.string(algo), 
            tag    = cms.string('%s_%s_%s' % (jec_type, ERA, algo)), 
            label  = cms.string(algo)
            )]

    setattr(process, 'dbWriter%s' % algo, cms.EDAnalyzer('JetCorrectorDBWriter',
        era    = cms.untracked.string(ERA), 
        algo   = cms.untracked.string(algo),
        path   = cms.untracked.string(options.path)
        )
        )

    sequence += getattr(process, 'dbWriter%s' % algo)


process.p = cms.Path(sequence)
