from test import * 
import pandas as pd

import sys
from numpy import indices, size
from sympy import false, true
from torch import log2_
from HLT_Study import *
from L1_HLT_cut import *
from emulation import * 
# Feature extraction

def features():
  # class label, lepton 1 pT, lepton 1 eta, lepton 1 phi, lepton 2 pT, 
  # lepton 2 eta, lepton 2 phi, missing energy magnitude, missing energy phi, 
  # MET_rel, axial MET, M_R, M_TR_2, R, MT2, S_R, M_Delta_R, dPhi_r_b, cos(theta_r1)
  df = pd.read_csv("../data/HIGGS_10K.csv",names=('isSignal',
      'lep1_pt','lep1_eta','lep1_phi','miss_ene' ,'miss_ene_phi', 
      'jet_1_pt', 'jet_1_eta', 'jet_1_phi', 'jet_1_b_tag',
      'jet_2_pt', 'jet_2_eta', 'jet_2_phi', 'jet_2_b_tag',
      'jet_3_pt', 'jet_3_eta', 'jet_3_phi', 'jet_3_b_tag',
      'jet_4_pt', 'jet_4_eta', 'jet_4_phi', 'jet_4_b_tag',
      'm_jj', 'm_jjj', 'm_lv', 'm_jlv', 'm_bb', 'm_wbb', 'm_wwbb' ))
  
  df_test = pd.read_csv("../data/HIGGS_1K.csv",names=('isSignal',
      'lep1_pt','lep1_eta','lep1_phi','miss_ene' ,'miss_ene_phi', 
      'jet_1_pt', 'jet_1_eta', 'jet_1_phi', 'jet_1_b_tag',
      'jet_2_pt', 'jet_2_eta', 'jet_2_phi', 'jet_2_b_tag',
      'jet_3_pt', 'jet_3_eta', 'jet_3_phi', 'jet_3_b_tag',
      'jet_4_pt', 'jet_4_eta', 'jet_4_phi', 'jet_4_b_tag',
      'm_jj', 'm_jjj', 'm_lv', 'm_jlv', 'm_bb', 'm_wbb', 'm_wwbb' ))

  feature_dim = 3  # dimension of each data point

  # Leptonic features
  X1 = df[['lep1_pt','lep1_eta','lep1_phi']] 


  # jet1 representations
  X2 = df[['jet_1_pt', 'jet_1_eta', 'jet_1_phi', 'jet_1_b_tag']]
  X3 = df[['jet_2_pt', 'jet_2_eta', 'jet_2_phi', 'jet_2_b_tag']]
  X4 = df[['jet_3_pt', 'jet_3_eta', 'jet_3_phi', 'jet_3_b_tag']]
  X5 = df[['jet_4_pt', 'jet_4_eta', 'jet_4_phi', 'jet_4_b_tag']]

  # invariant mass
  X1 = X1.to_numpy()
  X2 = X2.to_numpy()
  X3 = X3.to_numpy()
  X4 = X4.to_numpy()


  # Create histogram for the mapping
  hist_lep1_pt = ROOT.TH1D("lep1_pt", "", 20, 0 , 4)
  hist_lep1_eta = ROOT.TH1D("lep1_eta", "", 50, -5 , 5)
  hist_lep1_phi = ROOT.TH1D("lep1_phi", "", 25, -2.5 , 2.5)

  hist_jet1_pt = ROOT.TH1D("jet1_pt", "", 20, 0 , 4)
  hist_jet1_eta = ROOT.TH1D("jet1_eta", "", 50, -5 , 5)
  hist_jet1_phi = ROOT.TH1D("jet1_phi", "", 25, -2.5 , 2.5)

  hist_jet2_pt = ROOT.TH1D("jet2_pt", "", 20, 0 , 4)
  hist_jet2_eta = ROOT.TH1D("jet2_eta", "", 50, -5 , 5)
  hist_jet2_phi = ROOT.TH1D("jet2_phi", "", 25, -2.5 , 2.5)

  hist_jet3_pt = ROOT.TH1D("jet3_pt", "", 20, 0 , 4)
  hist_jet3_eta = ROOT.TH1D("jet3_eta", "", 50, -5 , 5)
  hist_jet3_phi = ROOT.TH1D("jet3_phi", "", 25, -2.5 , 2.5)

  for i in range(len(X3)):
    hist_lep1_pt.Fill(X1[i][0])
    hist_lep1_eta.Fill(X1[i][1])
    hist_lep1_phi.Fill(X1[i][2])

    hist_jet1_pt.Fill(X2[i][0])
    hist_jet1_eta.Fill(X2[i][1])
    hist_jet1_phi.Fill(X2[i][2])

    hist_jet2_pt.Fill(X3[i][0])
    hist_jet2_eta.Fill(X3[i][1])
    hist_jet2_phi.Fill(X3[i][2])

    hist_jet3_pt.Fill(X4[i][0])
    hist_jet3_eta.Fill(X4[i][1])
    hist_jet3_phi.Fill(X4[i][2])



  hist_print(hist_lep1_pt, 1, "pt", 20, 0 , 4)
  hist_print(hist_lep1_eta, 1, "eta", 50,-5,5)
  hist_print(hist_lep1_phi, 1, "phi", 25, -2.5 , 2.5)

  hist_print(hist_jet1_pt, 1, "pt", 20, 0 , 4)
  hist_print(hist_jet1_eta, 1, "eta", 50,-5,5)
  hist_print(hist_jet1_phi, 1, "phi", 25, -2.5 , 2.5)

  hist_print(hist_jet2_pt, 1, "pt", 20, 0 , 4)
  hist_print(hist_jet2_eta, 1, "eta", 50,-5,5)
  hist_print(hist_jet2_phi, 1, "phi", 25, -2.5 , 2.5)

  hist_print(hist_jet3_pt, 1, "pt", 20, 0 , 4)
  hist_print(hist_jet3_eta, 1, "eta", 50,-5,5)
  hist_print(hist_jet3_phi, 1, "phi", 25, -2.5 , 2.5)

  pt = []
  pt.append(hist_jet1_pt)
  pt.append(hist_jet2_pt)
  pt.append(hist_jet3_pt)
  pt.append(hist_lep1_pt)


  hist_print_compare( pt,
                ["jet1","jet2","jet3", "lep1"],
                "p_T", 0)




if __name__ == '__main__' :
  features()
  print("Done with ploting new features")