import pandas
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open("nano_files/qqH_GenPart.pkl", "r") as f:
    GenPart = pickle.load(f)
with open("nano_files/qqH_LHEPart_sumhel.pkl", "r") as f:
    LHEPart_sumhel = pickle.load(f)

w1 = GenPart.nano
w2 = GenPart.lhe
log_diffs = np.log10( abs((w1-w2)/w1) )
n, bins, patches = plt.hist(log_diffs, 50, (-10, 2), histtype='step', label="GenPart")

w1 = LHEPart_sumhel.nano
w2 = LHEPart_sumhel.lhe
log_diffs = np.log10( abs((w1-w2)/w1) )
n, bins, patches = plt.hist(log_diffs, 50, (-10, 2), histtype='step', label="LHEPart_sumhel")

label1 = "w"
label2 = "w_{lhe}"
plt.xlabel(r"$log_{10}(|(%s-%s)/%s|)$"%(label1, label2, label1))

plt.legend()

plt.savefig("GenPart_vs_LHEPart_sumhel.png")
plt.savefig("GenPart_vs_LHEPart_sumhel.pdf")
plt.clf()

