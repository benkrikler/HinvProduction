import FWCore.ParameterSet.Config as cms

# link to card:
# https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/VH_from_Hbb/HZJ_HanythingJ_NNPDF30_13TeV_M110_Vhadronic.input

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
#    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF30_13TeV_M110_Vhadronic_HZJ/v1/HZJ_HanythingJ_NNPDF30_13TeV_M110_Vhadronic_HZJ.tgz'),
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic/v2/HZJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic.tgz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


# Based on https://github.com/cms-sw/genproductions/blob/3b33b1e47f34941b84b6a582839bb8e5c5b05c16/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_powhegEmissionVeto_1p_LHE_pythia8_cff.py

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 3',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
            '25:m0 = 125.0',
            '25:onMode = off',
            '25:onIfMatch = 23 23', ## H -> ZZ
            '23:onMode = off',      # turn OFF all Z decays
            '23:onIfAny = 12 14 16',# turn ON Z->vv
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
				    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
