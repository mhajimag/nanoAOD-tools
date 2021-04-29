from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import numpy as np

class exampleProducer(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("m12", "F")
        self.out.branch("m34", "F")
        self.out.branch("selected", "O")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def dR(self, l1, l2):
      d_eta = l1.eta - l2.eta
      d_phi = l1.phi - l2.phi
      return np.sqrt(d_eta**2 + d_phi**2)

    def select(self, ZZ):
      l1, l2, l3, l4 = ZZ[0][0], ZZ[0][1], ZZ[1][0], ZZ[1][1]
      ls = [l1,l2,l3,l4]
      Z1 = ZZ[0][0].p4() + ZZ[0][1].p4()
      Z2 = ZZ[1][0].p4() + ZZ[1][1].p4()

      #Z cuts
      if Z1.M()<12 or Z1.M()>120:
        return False
      if Z2.M()<12 or Z2.M()>120:
        return False

      #mll cut
      if l1.charge==-l3.charge:
        mll1 = (l1.p4() + l3.p4()).M()
        mll2 = (l2.p4() + l4.p4()).M()
      else:
        mll1 = (l1.p4() + l4.p4()).M()
        mll2 = (l2.p4() + l3.p4()).M()
      
      if mll1<4 or mll2<4:
        return False

      #m4l cut
      if (Z1 + Z2).M() < 70:
        return False
      
      #lepton pt and eta cuts
      ngt20 = 0
      ngt10 = 0
      for l in ls:
        if abs(l.pdgId)==11:
          if l.pt<7 or abs(l.eta)>2.5:
            return False
        else:
          if l.pt<5 or abs(l.eta)>2.4:
            return False
        
        if l.pt>20:
          ngt20 += 1
          ngt10 += 1
        elif l.pt>10:
          ngt10 += 1
      
      if ngt20<1 or ngt10<2:
        return False
      
      #lepton isolation cuts
      for i in range(4):
        for j in range(i+1, 4):
          if self.dR(ls[i], ls[j])<0.02:
            return False

      #if at this point, event has passed
      #print("passed!")
      return True      

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        
        Z_candidates = []
        #make Z->ee candidates
        for i in range (len(electrons)):
          for j in range(i+1, len(electrons)):
            e1, e2 = electrons[i], electrons[j]
            if e1.charge==-e2.charge:
                Z_candidates.append([e1,e2])

        #make Z->mu mu candidates
        for i in range (len(muons)):
          for j in range(i+1, len(muons)):
            mu1, mu2 = muons[i], muons[j]
            if mu1.charge==-mu2.charge:
              Z_candidates.append([mu1, mu2])

        #find closest and second closest Z candiates
        #print(len(Z_candidates))
        if len(Z_candidates)>=2:
          selected_candidates = [None, None]
          m12 = -9999
          m34 = -9999
          for cand in Z_candidates:
            inv_m = (cand[0].p4() + cand[1].p4()).M()
            if abs(inv_m-91.18)<abs(m12-91.18):
              m34 = m12
              m12 = inv_m
              selected_candidates[1] = selected_candidates[0]
              selected_candidates[0] = cand
            elif abs(inv_m-91.18)<abs(m34-91.18):
              m34 = inv_m
              selected_candidates[1] = cand
        
          self.out.fillBranch("m12", m12)
          self.out.fillBranch("m34", m34)
          self.out.fillBranch("selected", self.select(selected_candidates))   
          return True
        else:
          return False
