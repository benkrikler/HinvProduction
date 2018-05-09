#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
if [ -r CMSSW_8_0_21/src ] ; then 
 echo release CMSSW_8_0_21 already exists
else
scram p CMSSW CMSSW_8_0_21
fi
cd CMSSW_8_0_21/src
eval `scram runtime -sh`


scram b
cd ../../
cmsDriver.py step1 --filein "dbs:/ZH_HToInvisible_ZToQQ_M110_13TeV_powheg_pythia8/RunIISummer15wmLHEGS-MCRUN2_71_V1-v1/GEN-SIM" --fileout file:HIG-RunIISummer16DR80Premix-01471_step1.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename HIG-RunIISummer16DR80Premix-01471_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 169 || exit $? ; 

cmsDriver.py step2 --filein file:HIG-RunIISummer16DR80Premix-01471_step1.root --fileout file:HIG-RunIISummer16DR80Premix-01471.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename HIG-RunIISummer16DR80Premix-01471_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 169 || exit $? ; 

