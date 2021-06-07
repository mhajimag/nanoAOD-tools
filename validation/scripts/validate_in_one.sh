#!/usr/bin/env bash

set -x
set -e

#source /cvmfs/cms.cern.ch/cmsset_default.sh

LHE_PATH=$1
NEVENTS=$2
RW_PATH=$3
METHOD=$4
PLOTS_DIR=$5

if [ -z "$6" ]; then
    WORKDIR=${TMPDIR}
else
    WORKDIR=$6
fi
echo "Using ${WORKDIR} as working directory."

EDM_PATH=${WORKDIR}/edm.root
NANOGEN_PATH=${WORKDIR}/nanogen.root
EFT2OBS_PKL_PATH=${WORKDIR}/eft2obs.pkl

cmsDriver.py --python_filename ${WORKDIR}/lhe_edm.py --eventcontent LHE --datatier LHE \
    --fileout file:$EDM_PATH --conditions auto:mc --step NONE --filein file:$LHE_PATH \
    --no_exec --mc -n $NEVENTS

cmsDriver.py PhysicsTools/NanoAODTools/python/postprocessing/modules/reweighting/hadronizer.py \
    --filein file:$EDM_PATH --fileout $NANOGEN_PATH --mc --eventcontent NANOAODGEN \
    --datatier NANOAODSIM --conditions auto:mc --step GEN,NANOGEN --nThreads 1 \
    --python_filename ${WORKDIR}/edm_nano.py --no_exec -n $NEVENTS \
    --customise PhysicsTools/NanoAOD/nanogen_cff.pruneGenParticlesNano 
#PhysicsTools/NanoAOD/nanogen_cff.setLHEFullPrecision 


cmsRun ${WORKDIR}/lhe_edm.py
cmsRun ${WORKDIR}/edm_nano.py

{
    echo "keep *"
} > ${WORKDIR}/keep_and_drop_input.txt
{
    echo "drop *"
    echo "keep Reweights"
    echo "keep LHEPart_incomingpz"
} > ${WORKDIR}/keep_and_drop_output.txt

python ../scripts/run_reweighting.py ${WORKDIR} $NANOGEN_PATH $RW_PATH -s _reweighted \
    --bi ${WORKDIR}/keep_and_drop_input.txt --bo ${WORKDIR}/keep_and_drop_output.txt -m $METHOD

python scripts/eft2obs_only_test.py $LHE_PATH $RW_PATH $EFT2OBS_PKL_PATH $NEVENTS
python scripts/validate_nano.py $EFT2OBS_PKL_PATH ${WORKDIR}/nanogen_reweighted.root $PLOTS_DIR