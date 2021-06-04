import sys
import lhe_interface
import numpy as np
#import standalone_reweight
import PhysicsTools.NanoAODTools.postprocessing.modules.reweighting.standalone_reweight as standalone_reweight
from collections import OrderedDict
import pandas
import pickle

if __name__=="__main__":
  filename = sys.argv[1]
  process = sys.argv[2]
  pkl_save = sys.argv[3]
  n_events = int(sys.argv[4])
  
  rw = standalone_reweight.StandaloneReweight(process)
  n_rw = rw.N

  print("Getting reweights from LHE file")
  fromfile_weights_gen = lhe_interface.getReweightsFromFile(filename, n_rw, False)
  #all_weights = [w for w in fromfile_weights_gen]
  all_weights = [next(fromfile_weights_gen) for i in range(n_events)]

  sm_w = all_weights[0][0]

  #n_events = len(all_weights)

  event_id = np.array([i for i in range(n_events) for j in range(n_rw)])
  rw_id = np.array([i for j in range(n_events) for i in range(n_rw)])
  lhe_reweights = np.array(all_weights).flatten()

  data = OrderedDict([("eid",event_id),
                      ("rid",rw_id),
                      ("lhe",lhe_reweights)])

  print("Performing reweighting using standalone module")
  rounding = None
  event_gen = lhe_interface.getEvents(filename, rounding)
  all_events = [next(event_gen) for i in range(n_events)]
  all_calculated_weights = [event.getReweights(rw) for event in all_events]
  all_calculated_weights = np.array(all_calculated_weights)*sm_w
  data["EFT2Obs_%s"%str(rounding)] = all_calculated_weights.flatten()

  incomingpz_1 = [event.getParticles()[0].getP()[3] for event in all_events]
  incomingpz_2 = [event.getParticles()[1].getP()[3] for event in all_events]
  incomingpz = OrderedDict([("incomingpz_1",incomingpz_1),
                            ("incomingpz_2",incomingpz_2)])

  #for rounding in [8, 7, 6, 5, 4, 3, 2]:
  for rounding in [4, 3, 2]:
    print("Round: %s"%str(rounding))
    event_gen = lhe_interface.getEvents(filename, rounding)
    all_events = [next(event_gen) for i in range(n_events)]
    all_calculated_weights = [event.getReweights(rw) for event in all_events]
    all_calculated_weights = np.array(all_calculated_weights)*sm_w
    data["EFT2Obs_%s"%str(rounding)] = all_calculated_weights.flatten()

  weights_df = pandas.DataFrame(data)
  incomingpz_df = pandas.DataFrame(incomingpz)

  with open(pkl_save, "w") as f:
    pickle.dump((weights_df, incomingpz_df), f)


  

  