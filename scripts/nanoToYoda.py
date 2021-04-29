#fill in yoda histogram with nanoAOD
import uproot
import yoda
import sys
import numpy as np
import awkward as ak

filename = sys.argv[1]
outname = sys.argv[2]

f = uproot.open(filename)
stxs=f["Events"]["HTXS_stage1_2_cat_pTjet30GeV"].array()
reweights=f["Events"]["Reweights"].array()

n_events = len(reweights)
n_rw = len(reweights[0])
n_pars = int((-3 + np.sqrt(9+8*(n_rw-1)))/2)

hists = []
for i in range(n_rw):
  hists.append(yoda.Histo1D(6,600,606, "/HiggsTemplateCrossSections/HTXS_stage1_2_pTjet30[rw%.4i]"%i))

for i in range(n_events):
  if (i%10000 == 0):
    print("Processed %d/%d events"%(i, n_events))
  inw = ak.to_numpy(reweights[i])
  out = inw.copy()
  for ip in range(n_pars):
    s0 = inw[0]
    s1 = inw[ip*2 + 1]
    s2 = inw[ip*2 + 2]
    s1 -= s0
    s2 -= s0
    Ai = 4. * s1 - s2
    Bii = s2 - Ai

    out[ip*2 + 1] = Ai
    out[ip*2 + 2] = Bii
 
  crossed_offset = 1 + 2*n_pars
  c_counter = 0
  for ix in range(n_pars):
    for iy in range(ix+1, n_pars):
      s = inw[crossed_offset + c_counter]
      sm = inw[0]
      sx = out[ix*2 + 1]
      sy = out[iy*2 + 1]
      sxx = out[ix*2 + 2]
      syy = out[iy*2 + 2]
      s -= (sm + sx + sy + sxx + syy)
      out[crossed_offset + c_counter] = s
      c_counter += 1

  for j in range(n_rw):
    hists[j].fill(stxs[i], out[j])  

yoda.write(hists, outname)