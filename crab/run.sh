#!/bin/bash

set -x
#set -e

outDir=$1
in_file=$2
rw_path=$3
start=$4
entries=$5

if [[ -n $6 ]]; then
    export X509_USER_PROXY=$6
    voms-proxy-info -all
    voms-proxy-info -all -file $6
fi

if [[ -n $7 && -n $8 ]]; then
    ClusterId=$7
    ProcId=$8
else
    ClusterId=local
    ProcId=run
fi

cd /afs/cern.ch/user/m/mknight/private/CMSSW_10_6_8/src/PhysicsTools/NanoAODTools
source /cvmfs/cms.cern.ch/cmsset_default.sh 
eval `scramv1 runtime -sh`

postfix=${ClusterId}_${ProcId}

python scripts/run_reweighting.py ${TMPDIR} ${in_file} ${rw_path} --first-entry ${start} -N ${entries} -s ${postfix} -m ttH 

mkdir -p ${outDir}
cp ${TMPDIR}/*${postfix}.root ${outDir}/${postfix}.root

#split=$(echo $in_file | tr "/" "\n")
#for s in $split
#do
#    filename=$s
#done