#!/bin/bash

set -x
#set -e

export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1

in_file=$2
entries=$3
start=$4

cd /eos/home-m/mknight/dev/CMSSW_10_6_8/src/PhysicsTools/NanoAODTools
source /cvmfs/cms.cern.ch/cmsset_default.sh 
eval `scramv1 runtime -sh`

#in_file=root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/9646BBBF-8A18-F345-9E84-A15B6BA628A8.root
rw_path=/afs/cern.ch/user/m/mknight/private/EFT_Reweighting/rw_modules/rw_ggFfull-SMEFTsim_cHG

python scripts/run_reweighting.py ${TMPDIR} ${in_file} ${rw_path} lhe ${entries} 0 ${start}

cp ${TMPDIR}/9646BBBF-8A18-F345-9E84-A15B6BA628A8_Skim.root /eos/home-m/mknight/dev/CMSSW_10_6_8/src/PhysicsTools/NanoAODTools/ggF_Skim.root

