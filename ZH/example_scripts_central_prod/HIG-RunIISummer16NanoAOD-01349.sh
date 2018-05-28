#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc630
if [ -r CMSSW_9_4_4/src ] ; then 
 echo release CMSSW_9_4_4 already exists
else
scram p CMSSW CMSSW_9_4_4
fi
cd CMSSW_9_4_4/src
eval `scram runtime -sh`


scram b
cd ../../
cmsDriver.py step1 --filein "dbs:/ZH_HToInvisible_ZToQQ_M110_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" --fileout file:HIG-RunIISummer16NanoAOD-01349.root --mc --eventcontent NANOEDMAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v2 --step NANO --nThreads 2 --era Run2_2016,run2_miniAOD_80XLegacy --python_filename HIG-RunIISummer16NanoAOD-01349_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10000 || exit $? ; 

