#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
if [ -r CMSSW_7_1_24/src ] ; then 
 echo release CMSSW_7_1_24 already exists
else
scram p CMSSW CMSSW_7_1_24
fi
cd CMSSW_7_1_24/src
eval `scram runtime -sh`

curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer15wmLHEGS-00328 --retry 2 --create-dirs -o Configuration/GenProduction/python/HIG-RunIISummer15wmLHEGS-00328-fragment.py 
[ -s Configuration/GenProduction/python/HIG-RunIISummer15wmLHEGS-00328-fragment.py ] || exit $?;

scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/HIG-RunIISummer15wmLHEGS-00328-fragment.py --fileout file:HIG-RunIISummer15wmLHEGS-00328.root --mc --eventcontent RAWSIM,LHE --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step LHE,GEN,SIM --magField 38T_PostLS1 --python_filename HIG-RunIISummer15wmLHEGS-00328_1_cfg.py --no_exec -n 64 || exit $? ; 

