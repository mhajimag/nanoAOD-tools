import sys
import os
import uproot as ur
import ROOT
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT.gROOT.ProcessLine('#include "LHEF.h"')
import numpy as np
import pandas as pd
from collections import OrderedDict
import pickle

def getNanoReweights(filename):
  f = ur.open(filename)
  reweights = f["Events"]["Reweights"].array(library='np')
  return reweights

def getNanoIncomingPz(filename):
  f = ur.open(filename)
  incomingpz = f["Events"]["LHEPart_incomingpz"].array()
  return np.array(incomingpz[:,:2])

def plotDiffGraph(w1, w2, save=True, suffix=""):
  log_diffs = np.log10( abs((w1-w2)/w1) )
  n, bins, patches = plt.hist(log_diffs, 50, (-10, 2), histtype='step')

  label1 = "w_{%s}"%w1.name
  label2 = "w_{%s}"%w2.name
  plt.xlabel(r"$log_{10}(|(%s-%s)/%s|)$"%(label1, label2, label1))

  largest_log_diff = log_diffs.max()
  largest_diff = np.power(10, largest_log_diff)

  plt.text(0.0,1.02, "Max difference: %.1f%%"%(largest_diff*100), transform=plt.gca().transAxes)
  plt.text(0.45,1.02, "No. events outside 1%%: %d / %d"%(sum(log_diffs>-2), len(log_diffs)), transform=plt.gca().transAxes)

  if save:
    save_path = plots_dir+"%s_%s"%(w1.name, w2.name)
    plt.savefig(save_path+suffix+".png")
    plt.savefig(save_path+suffix+".pdf")
    plt.clf()

def logDiffs(w1, w2, w3):
  diffs1 = abs((w1-w2)/w1)
  selection = diffs1>1e-12
  log_diffs1 = np.log10(diffs1[selection])

  diffs2 = abs((w1-w3)/w1)
  log_diffs2 = np.log10(diffs2[selection])
  return log_diffs1, log_diffs2

def checkIncomingPz(lhe_incomingpz, nano_incomingpz, w):
  """When using jet matching, events will be missing -> filter through and match
  according to incomingpz."""
  print("Number of events in lhe: %d"%len(lhe_incomingpz))
  print("Number of events in nano: %d"%len(nano_incomingpz))

  to_drop = w.eid>-1 #initialise selection to select all events

  nano_index = 0
  for i in range(len(lhe_incomingpz)):
    #check if there is a match
    lpz1, lpz2 = lhe_incomingpz.iloc[i].incomingpz_1, lhe_incomingpz.iloc[i].incomingpz_2
    npz1, npz2 = nano_incomingpz[nano_index,0], nano_incomingpz[nano_index,1]
    is_not_same1 = (lpz1-npz1)/lpz1 > 0.001
    is_not_same2 = (lpz2-npz2)/lpz2 > 0.001
    if is_not_same1 or is_not_same2: #if not a match
      to_drop = (to_drop)|(w.eid==i) #delete this entry in the weights df
    else: #if match
      nano_index += 1
  
  w = w[to_drop]
  if len(w)==0:
    raise Exception("All events have been cut out.")
  else:
    return w


if __name__ == "__main__":
  eft2obs_pkl_path = sys.argv[1]
  nano_path = sys.argv[2]
  plots_dir = sys.argv[3]

  if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

  with open(eft2obs_pkl_path, "r") as f:
    print("Loading eft2obs pkl file...")
    w, lhe_incomingpz = pickle.load(f)

  n_rw = len(w.rid.unique())
  n_events = len(w.eid.unique())
  
  print("Reading nano...")
  nano_reweights = getNanoReweights(nano_path)
  nano_incomingpz = getNanoIncomingPz(nano_path)

  #check that for each event the incomingpz agree
  lpz1, lpz2 = lhe_incomingpz.incomingpz_1, lhe_incomingpz.incomingpz_2
  npz1, npz2 = nano_incomingpz[:,0], nano_incomingpz[:,1]
  is_not_same1 = (lpz1-npz1)/lpz1 > 0.001
  is_not_same2 = (lpz2-npz2)/lpz2 > 0.001
  if sum(is_not_same1) + sum(is_not_same2) > 0:
    raise Exception("Incomingpz did not agree")
  
  #w = checkIncomingPz(lhe_incomingpz, nano_incomingpz, w)
 
  w["nano"] = nano_reweights.flatten()
 
  with open(nano_path[:-5]+".pkl", "w") as f:
    pickle.dump(w, f)

  for column in w.columns:
    if column not in ["eid", "rid", "lhe"]:
      plotDiffGraph(w["lhe"], w[column])
  
  #plot only rw that change
  rid_include = [1,2,3,4,7,8,9,10,11,12,17,18,21,22,23,24,29,30]
  sw = w[w.rid.isin(rid_include)]
  for column in sw.columns:
    if column not in ["eid", "rid", "lhe"]:
      plotDiffGraph(sw["lhe"], sw[column], suffix="_selected_parameters")

  sw - w[w.rid<=30]
  for rid in sw.rid.unique():
    ssw = sw[sw.rid==rid]
    plotDiffGraph(ssw["lhe"], ssw["nano"], suffix="_rw_%d"%rid)

  log_diffs1, log_diffs2 = logDiffs(w.lhe, w.EFT2Obs_2, w.nano)
  plt.hist(log_diffs1, 50, (-10, 2), alpha=0.5, label="EFT2Obs round 2 d.p", histtype='step')
  plt.hist(log_diffs2, 50, (-10, 2), alpha=0.5, label="Nano", histtype='step')
  plt.xlabel(r"$log_{10}(|(w-w_{lhe})/w_{lhe}|)$")
  plt.legend()
  plt.savefig(plots_dir+"comparison_2.png")
  plt.savefig(plots_dir+"comparison_2.pdf")
  plt.clf()

  log_diffs1, log_diffs2 = logDiffs(w.lhe, w.EFT2Obs_3, w.nano)
  plt.hist(log_diffs1, 50, (-10, 2), alpha=0.5, label="EFT2Obs round 3 d.p", histtype='step')
  plt.hist(log_diffs2, 50, (-10, 2), alpha=0.5, label="Nano", histtype='step')
  plt.xlabel(r"$log_{10}(|(w-w_{lhe})/w_{lhe}|)$")
  plt.legend()
  plt.savefig(plots_dir+"comparison_3.png")
  plt.savefig(plots_dir+"comparison_3.pdf")
  plt.clf()
  
  """
  for rid in w.rid.unique():
    print(rid, w[w.rid==rid].nano.mean())
  """

  


