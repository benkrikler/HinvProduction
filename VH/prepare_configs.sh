#!/bin/bash
ScriptDir="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
echo $ScriptDir
ProdMode="$1" ; shift
BuildDir="$1"
if [ -z "$ProdMode" ] ; then
	echo "No Higgs production mode given"
    exit 1
elif [ "${ProdMode^^}" == WPLUSH ];then
    GridPack=/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/HWplusJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic/v2/HWplusJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic.tgz
elif [ "${ProdMode^^}" == WMINUSH ];then
    GridPack=/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/HWminusJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic/v2/HWminusJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic.tgz
elif [ "${ProdMode^^}" == ZH ];then
    GridPack=/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/HZJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic/v2/HZJ_HanythingJ_NNPDF30_13TeV_M125_Vhadronic.tgz
else
    echo "No valid gridpack for $ProdMode"
    exit 1
fi

BuildDir="${BuildDir:-build_$ProdMode}"
mkdir -p "$BuildDir"
cd "$BuildDir"

source /cvmfs/cms.cern.ch/cmsset_default.sh
voms-proxy-init --voms cms -rfc

function setup_cmssw(){
    export SCRAM_ARCH="$1"; shift
    local version="$1"; shift
    if [ -r "$version"/src ] ; then 
     echo release $version already exists
    else
    scram p CMSSW "$version"
    fi
    cd "$version"/src
    eval `scram runtime -sh`
    [ -n "$PostSetup" ] && $PostSetup && unset PostSetup
    scram b
    cd ../../
}

function next_file_out(){
    FILE_IN="$FILE_OUT"
    FILE_OUT=output_"$1".root
}

# ===  LHE
function post_setup_lhe(){
pwd
ls 
    mkdir -p Configuration/GenProduction/python
    sed -e 's!%%GRIDPACK%%!'$GridPack'!g' "$ScriptDir"/LHE_step_fragment.py  > Configuration/GenProduction/python/LHE_step_fragment.py
    [ -s Configuration/GenProduction/python/LHE_step_fragment.py ] || exit $?;
}
function config_lhe(){
echo ======== Now running: LHE
PostSetup=post_setup_lhe
setup_cmssw slc6_amd64_gcc481 CMSSW_7_1_24

cmsDriver.py Configuration/GenProduction/python/LHE_step_fragment.py\
           --fileout file:$FILE_OUT\
           --mc --eventcontent RAWSIM,LHE\
           --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring\
           --datatier GEN-SIM,LHE --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision\
           --step LHE,GEN,SIM --magField 38T_PostLS1\
           --python_filename driver_cfg_LHE.py --no_exec -n 20 || exit $?
}

# ===  Premix
function config_premix(){
echo ======== Now running: Premix
setup_cmssw slc6_amd64_gcc530 CMSSW_8_0_21

cmsDriver.py step1 --filein "file:$FILE_IN"\
           --fileout file:output_premix_interm.root\
           --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW"\
           --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6\
           --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix\
           --era Run2_2016 --python_filename driver_cfg_premix_step1.py\
           --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1 || exit $? ; 

cmsDriver.py step2 --filein file:output_premix_interm.root\
           --fileout file:$FILE_OUT\
           --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM\
           --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI\
           --nThreads 4 --era Run2_2016 --python_filename driver_cfg_premix_step2.py\
           --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1 || exit $? ; 
}

# ===  Miniaod
function config_miniaod(){
echo ======== Now running: MiniAOD
setup_cmssw slc6_amd64_gcc530 CMSSW_8_0_21

cmsDriver.py step1 --filein "file:$FILE_IN" --fileout file:$FILE_OUT\
           --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM\
           --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016\
           --python_filename driver_cfg_miniaod.py\
           --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1 || exit $? ; 
}

# ===  Nanoaod
function config_nanoaod(){
echo ======== Now running: NanoAOD
setup_cmssw slc6_amd64_gcc630 CMSSW_9_4_9

cmsDriver.py step1 --filein "file:$FILE_IN"\
           --fileout file:$FILE_OUT\
           --mc --eventcontent NANOAODSIM --datatier NANOAODSIM\
           --conditions 94X_mcRun2_asymptotic_v2 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy\
           --python_filename driver_cfg_nanoaod.py --no_exec\
           --customise Configuration/DataProcessing/Utils.addMonitoring -n -1 || exit $? ; 
}

next_file_out lhe
( config_lhe )
next_file_out premix
( config_premix )
next_file_out miniaod
( config_miniaod )
next_file_out nanoaod
( config_nanoaod )
