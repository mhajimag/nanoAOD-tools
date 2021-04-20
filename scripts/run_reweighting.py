#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import PhysicsTools.NanoAODTools.postprocessing.modules.reweighting.reweighter as rw

if __name__ == "__main__":
    outdir = sys.argv[1]
    input_file = [sys.argv[2]]
    rw_path = sys.argv[3]
    lhe_or_gen = sys.argv[4]
    try:
        entries = int(sys.argv[5])
    except:
        entries = None
    try:
        verb = int(sys.argv[6])
    except:
        verb = False
      

    if lhe_or_gen=="lhe":
        modules = [rw.LHEReweighter(rw_path, verb=verb)]
    elif lhe_or_gen=="gen":
        modules = [rw.GenReweighter(rw_path,verb=verb)]
    elif lhe_or_gen=="higgsdecay":
        modules = [rw.HiggsDecayReweighter(rw_path, verb=verb)]
    elif lhe_or_gen=="h4l":
        modules = [rw.H4LReweighter(rw_path, verb=verb)]
    else:
        raise Exception("Invalid reweighting type")

    p = PostProcessor(outdir, input_file,
                      modules=modules,
                      maxEntries=entries,
                      branchsel="keep_and_drop_input.txt",
                      outputbranchsel="keep_and_drop_output.txt")
    p.run()
