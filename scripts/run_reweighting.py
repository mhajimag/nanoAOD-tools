#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import warnings
import PhysicsTools.NanoAODTools.postprocessing.modules.reweighting.reweighter as rw

def checkKeepDrop(keep_drop_input, keep_drop_output, method):
    check_for = ["keep LHE_AlphaS", "keep genWeight", "keep LHEPart*", "keep GenPart*", "keep Generator*"]
    found = [False for check in check_for]
    
    with open(keep_drop_input, "r") as f:
        lines = []
        for line in f:
            if line=="keep *\n":
                return None
            for i, check in enumerate(check_for):
                if check==line.strip("\n"):
                    found[i] = True

    if method == "LHE":
        expected = [0,1,2]
    elif method == "Gen":
        expected = [0,1,3,4]
    else:
        expected = [0,1,2,3,4]

    not_found = []
    for i in expected:
        if not found[i]:
            not_found.append(check_for[i].strip(" keep"))
    if len(not_found) > 0:
        not_found_str = ", ".join(not_found)
        warnings.warn("Selected input branches may be incompatible with chosen reweighting method. Missing branches appear to be: %s. Please check your keep_and_drop_input.txt ."%not_found_str)

    found_Reweights = False
    check_for = ["keep Reweights", "keep *"]
    with open(keep_drop_output, "r") as f:
        for line in f:
            if line.strip("\n") in check_for:
                found_Reweights = True
        
    if not found_Reweights:
        warnings.warn("Looks like the 'Reweights' branch is missing from the outputted branches. Please check your keep_and_drop_output.txt .")

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles rw_path")
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default=None,
                      help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json", dest="json", type="string",
                      default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut", dest="cut", type="string",
                      default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection", dest="branchsel",
                      type="string", default=None, help="Branch selection")
    parser.add_option("--bi", "--branch-selection-input", dest="branchsel_in",
                      type="string", default="scripts/keep_and_drop_input.txt", help="Branch selection input")
    parser.add_option("--bo", "--branch-selection-output", dest="branchsel_out",
                      type="string", default="scripts/keep_and_drop_output.txt", help="Branch selection output")
    parser.add_option("--friend", dest="friend", action="store_true", default=False,
                      help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full", dest="friend", action="store_false", default=False,
                      help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout", dest="noOut", action="store_true",
                      default=False, help="Do not produce output, just run modules")
    parser.add_option("-P", "--prefetch", dest="prefetch", action="store_true", default=False,
                      help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true", default=False,
                      help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount", dest="justcount", default=False,
                      action="store_true", help="Just report the number of selected events")
    parser.add_option("-I", "--import", dest="imports", type="string", default=[], action="append",
                      nargs=2, help="Import modules (python package, comma-separated list of ")
    parser.add_option("-z", "--compression", dest="compression", type="string",
                      default=("LZMA:9"), help="Compression: none, or (algo):(level) ")

    parser.add_option("-m", "--method", dest="method", type="string", default="LHE")     
    parser.add_option("-v", "--verbose", dest="verb", action="store_true", default=False)

    (options, args) = parser.parse_args()

    if options.friend:
        if options.cut or options.json:
            raise RuntimeError(
                "Can't apply JSON or cut selection when producing friends")

    if len(args) < 3:
        parser.print_help()
        sys.exit(1)
    outdir = args[0]
    input_files = [args[1]]
    rw_path = args[2]

    if options.branchsel != None:
        options.branchsel_in = options.branchsel
        options.branchsel_out = options.branchsel

    Reweighter = getattr(rw, options.method+"Reweighter")
    checkKeepDrop(options.branchsel_in, options.branchsel_out, options.method)

    modules = [Reweighter(rw_path, verb=options.verb)]

    p = PostProcessor(outdir, input_files,
                      cut=options.cut,
                      branchsel=options.branchsel_in,
                      modules=modules,
                      compression=options.compression,
                      friend=options.friend,
                      postfix=options.postfix,
                      jsonInput=options.json,
                      noOut=options.noOut,
                      justcount=options.justcount,
                      prefetch=options.prefetch,
                      longTermCache=options.longTermCache,
                      maxEntries=options.maxEntries,
                      firstEntry=options.firstEntry,
                      outputbranchsel=options.branchsel_out)
    p.run()
    
    