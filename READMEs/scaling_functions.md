# Deriving STXS scaling functions

[EFT2Obs](https://github.com/ajgilbert/EFT2Obs) is a framework designed primarily to derive scaling functions for EFT studies. It is possible to use this standalone reweighting and feed the output into the EFT2Obs framework to derive scaling functions. The advantage of doing this - as opposed to only using EFT2Obs - is that if you are reweighting fully-simulated NanoAOD, you can apply reco-level selection criteria such that the derived scaling functions take acceptance effects into account.

The EFT2Obs workflow can be summarised as:
1. Define process and reweighting points with the proc_card.dat and reweight_card.dat .
2. Make a gridpack from these cards.
3. Produce events with this gridpack. These events are reweighted, showered by Pythia, and are categorised by Rivet. The output is given by a yoda file which is essentially a collection of histograms.
4. Given this yoda file, the get_scaling.py script is used to derive the scaling functions.

Centrally-produced NanoAOD contains branches that tell you which STXS bin it belongs. So if you have used run_reweighting.py to produce a new NanoAOD file with reweights, you are at a stage that is equivalent to step 3. Then, you can use [nanoToYoda.py](scripts/nanoToYoda.py) to convert that NanoAOD file to a yoda file which can then be used as input to get_scaling.py .