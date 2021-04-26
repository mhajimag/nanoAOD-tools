#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import PhysicsTools.NanoAODTools.postprocessing.modules.reweighting.reweighter as rw

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFile rw_path")
    parser.add_option("-m", "--method", dest="method", type="string", default="lhe")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("-v", dest="verb", action="store_true", default=False)
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default="")

    (options, args) = parser.parse_args()
    outdir = args[0]
    input_files = [args[1]]
    rw_path = args[2]

    if options.method=="lhe":
        modules = [rw.LHEReweighter(rw_path, verb=options.verb)]
    elif options.method=="gen":
        modules = [rw.GenReweighter(rw_path,verb=options.verb)]
    elif options.method=="higgsdecay":
        modules = [rw.HiggsDecayReweighter(rw_path, verb=options.verb)]
    elif options.method=="h4l":
        modules = [rw.H4LReweighter(rw_path, verb=options.verb)]
    elif options.method=="ggF":
        modules = [rw.ggFReweighter(rw_path, verb=options.verb)]
    elif options.method=="ttH":
        modules = [rw.ttHReweighter(rw_path, verb=options.verb)]
    else:
        raise Exception("Invalid reweighting type")

    p = PostProcessor(outdir, input_files,
                      modules=modules,
                      maxEntries=options.maxEntries,
                      branchsel="scripts/keep_and_drop_input.txt",
                      outputbranchsel="scripts/keep_and_drop_output.txt",
                      firstEntry=options.firstEntry,
                      postfix=options.postfix)
    p.run()
