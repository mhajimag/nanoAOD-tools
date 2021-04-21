#fill in yoda histogram with nanoAOD
import uproot
import yoda
import sys

filename = sys.argv[1]

f = uproot.open(filename)
stxs=f["Events"]["HTXS_stage1_2_cat_pTjet30GeV"].array()
reweights=f["Events"]["Reweights"].array()
genWeight=f["Events"]["genWeight"].array()

n_events = len(reweights)
n_rw = len(reweights[0])
hists = []
for i in range(n_rw):
  hists.append(yoda.Histo1D(17,100,117, "/STXS[rw%.4i]"%i))

for i in range(n_events):
  hists[0].fill(stxs[i], reweights[i][0])
  for j in range(1):
    s0 = reweights[i][0]
    s1 = reweights[i][j*2 + 1]
    s2 = reweights[i][j*2 + 2]
    s1 -= s0
    s2 -= s0
    Ai = 4. * s1 - s2
    Bii = s2 - Ai
 
    hists[j*2 + 1].fill(stxs[i], Ai)
    hists[j*2 + 2].fill(stxs[i], Bii)

yoda.write(hists, "test.yoda")