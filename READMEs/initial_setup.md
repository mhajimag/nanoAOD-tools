# Initial Setup

## Installing EFT2Obs

Before setting up this repository, I suggest you first set up [EFT2Obs](https://github.com/ajgilbert/EFT2Obs) following the instructions on EFT2Obs's README. The set up may take a while. 

**IMPORTANT :** EFT2Obs is not designed to be run in a CMSSW and will fail in some cases if a CMSSW environment is set. Make sure CMSSW is not set when installing, otherwise you may need to reinstall. CMSSW must also not be set when running EFT2Obs.

## Installing (this fork of) nanoAOD-tools

This repository is a fork of [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools). Whilst [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools) may work on a number of CMSSW releases, this particular fork, and the additional reweighting features added, have only been tested and known to work on CMSSW_10_6_25. One known constraint is imposed by the validation procedure, which uses [NanoGen](https://twiki.cern.ch/twiki/bin/viewauth/CMS/NanoGen), which is supposed to work for "CMSSW_10_6_X for X >= 19, and for CMSSW_11_2_X for X >= 0_pre".

To set up the repository, follow these instructions:

```sh
cd $CMSSW_BASE/src
git clone https://github.com/MatthewDKnight/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
cmsenv
scram b
```

