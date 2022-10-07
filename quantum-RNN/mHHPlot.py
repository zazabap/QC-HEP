# Author: Shiwen An 
# Date: 2022/08/01
# Purpose: Add some codes for emulation different part

import sys
from numpy import indices, size
from sympy import false, true
from torch import log2_
from HLT_Study import *
from L1_HLT_cut import *
from emulation import * 

taus = ["r22_Pass", "r22_PassFail", "Tau0_Pass", "Tau0_PassFail"]
list_order = ["RNN_Score","Prong","Delta_R","p_T","Subleading"]

r_pt = [100, 0, 250]

emu_order = [
    "Pt",
    "PtdR",
    "RNN",
    "Pt+RNN",
    "Pt+RNN+Delta_R"
]

#These cuts all work on pt only
def tree_online_pt_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
            indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
            indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices
    
def tree_online_ptdR_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices

def tree_online_RNN_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices

def tree_online_dR_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            dR = vec0.DeltaR(vec1)
            if ( dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())           
    return indices 

def tree_online_RNNdR_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn == false ): continue
            dR = vec0.DeltaR(vec1)
            if ( rnn and dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())        
    return indices    

def tree_online_ptRNN_i(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices

def tree_online_ptRNNdR_3525(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices


def tree_online_ptRNNdR_eta_3525(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTetafl)) :
        if ( tree.TrigMatched_Taus_HLTetafl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTetafl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTetafl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTetafl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTetafl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTetafl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTetafl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTetafl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTetafl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTetafl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTetafl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 ) : 
                indices.add(tree.TrigMatched_Taus_HLTetafl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTetafl[j].Pt())
    return indices


def tree_online_ptRNNdR_or_3525(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTetafl)) :
        if ( tree.TrigMatched_Taus_HLTetafl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTetafl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTetafl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTetafl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTetafl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTetafl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTetafl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTetafl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTetafl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTetafl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTetafl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 ) : 
                indices.add(tree.TrigMatched_Taus_HLTetafl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTetafl[j].Pt())

    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())

    return indices


def tree_online_ptRNNdR_3020(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 30): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 20): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())
    return indices

def tree_online_ptRNNdR_eta_3020(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTetafl)) :
        if ( tree.TrigMatched_Taus_HLTetafl[i].Pt() < 30): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTetafl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTetafl[j].Pt() < 20): continue
            vec0 = tree.TrigMatched_Taus_HLTetafl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTetafl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTetafl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTetafl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTetafl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTetafl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTetafl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTetafl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 ) : 
                indices.add(tree.TrigMatched_Taus_HLTetafl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTetafl[j].Pt())
    return indices


def tree_online_ptRNNdR_or_3020(tree):
    indices = set()
    for i in range(len(tree.TrigMatched_Taus_HLTetafl)) :
        if ( tree.TrigMatched_Taus_HLTetafl[i].Pt() < 30): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTetafl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTetafl[j].Pt() < 20): continue
            vec0 = tree.TrigMatched_Taus_HLTetafl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTetafl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTetafl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTetafl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTetafl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTetafl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTetafl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTetafl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 ) : 
                indices.add(tree.TrigMatched_Taus_HLTetafl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTetafl[j].Pt())

    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 30): continue
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 20): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            passPt = true
            pt0 = tree.TrigMatched_Taus_HLTptfl[j].Pt()
            pt1 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
            rnn_m_0 = tree.TrigMatched_TauIDm_HLTptfl[j]
            rnn_m_1 = tree.TrigMatched_TauIDm_HLTptfl[i]
            rnn_l_0 = tree.TrigMatched_TauIDl_HLTptfl[j]
            rnn_l_1 = tree.TrigMatched_TauIDl_HLTptfl[i]
            rnn = rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1)
            if (rnn): passPtRNN = true
            else: continue
            dR = vec0.DeltaR(vec1)
            if (  dR> 0.3 and dR <3.0) : 
                indices.add(tree.TrigMatched_Taus_HLTptfl[i].Pt())
                indices.add(tree.TrigMatched_Taus_HLTptfl[j].Pt())

    return indices


def emulation_passed_taus_pt(input_root, t):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open(input_root, "READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())

    # This is the plot for mHH 
    hist_mHH_raw = ROOT.TH1D("mHH_raw", "", 150, 0, 1500)
    hist_mHH_select = ROOT.TH1D("mHH_select", "", 150, 0, 1500)
    hist_mHH = ROOT.TH1D("mHH", "", 150, 0, 1500)
    hist_mHH_ = ROOT.TH1D("mHH_", "", 150, 0, 1500)

    de = 0
    for entry in entries:
        tree.GetEntry(entry)
        L1_1 = getattr(tree, "L1_J25")
        L1_2 = getattr(tree, "L1_ETA25")
        # Bit confused about this point of trigger use
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "r22_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "Tau0_Pass":
            HLT_1 = getattr(tree, "HLT_J25_Tau0")
            HLT = "HLT_J25_Tau0"
        elif taus[t] == "Tau0_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_Tau0")
            HLT = "HLT_J25_Tau0"

        # Selection
        hist_mHH_raw.Fill(tree.truthmHH*0.001, 1)
        select = True
        select = select and (len(tree.Offline_Matched_Taus) >= 2)
        if(select):
            select = select and (tree.Offline_Matched_Taus[0].Pt() > 20)
            select = select and (tree.Offline_Matched_Taus[1].Pt() > 12)
        if(len(tree.Off_Matched_TauIDl)<2): continue
        for i in range(len(tree.Off_Matched_TauIDl)):
                # print(tree.Off_Matched_TauIDl[i])
                if(tree.Off_Matched_TauIDl[0] == True
                 and tree.Off_Matched_TauIDl[1] == True):
                    select = select 
                else:
                    select = False
        # select = select and (L1_1 or L1_2)

        if(select):
            de = de+1
            hist_mHH_select.Fill(tree.truthmHH*0.001, 1)
            i_ptRNNdR = tree_online_ptRNNdR_3525(tree)
            i_ptRNNdR_ = tree_online_ptRNNdR_3020(tree)
            i_ptRNNdR_eta = tree_online_ptRNNdR_eta_3525(tree)
            i_ptRNNdR_eta_ = tree_online_ptRNNdR_eta_3020(tree) 
            if true:
                if len(i_ptRNNdR) >0 or len(i_ptRNNdR_eta) >0  :
                    hist_mHH.Fill(tree.truthmHH*0.001, 1)
                if len(i_ptRNNdR_) >0 or len(i_ptRNNdR_eta_) >0 :
                    hist_mHH_.Fill(tree.truthmHH*0.001, 1)                

    print("denominator: ", de)
    mhh = []
    mhh.append(hist_mHH_raw)
    mhh.append(hist_mHH_select)
    mhh.append(hist_mHH_)
    mhh.append(hist_mHH)

    mhh_r = []
    mhh_r.append(hist_mHH_)
    mhh_r.append(hist_mHH)

    hist_print_compare( mhh,
                ["raw","select","30 20","35 25"],
                "p_T", t)
    hist_print_compare_ratio( mhh_r,
                ["30 20","35 25"],
                "p_T", t)



def posleg_(pos_x, pos_y, items):
    global l_x_min, l_x_max, l_y_min, l_y_max
    width_x = 0.275 
    depth_i = 0.05
    l_x_L = 0.145 
    l_x_R = 0.95
    l_x_C = (l_x_L+l_x_R)/2
    l_y_D = 0.15
    l_y_U = 0.95 
    l_y_M = (l_y_D+l_y_U)/2 
    depth_y = items*depth_i
    if pos_x == "L":
        l_x_min = l_x_L
        l_x_max = l_x_L+width_x
    elif pos_x == "C":
        l_x_min = l_x_C-width_x/2
        l_x_max = l_x_C+width_x/2
    elif pos_x == "R":
        l_x_min = l_x_R-width_x
        l_x_max = l_x_R
    if pos_y == "D":
        l_y_min = l_y_D
        l_y_max = l_y_D+depth_y
    elif pos_y == "M":
        l_y_min = l_y_M-depth_y/2
        l_y_max = l_y_M+depth_y/2
    elif pos_y == "U":
        l_y_min = l_y_U-depth_y
        l_y_max = l_y_U

def hist_print_mHH(hist, x_label, x_div, x_min, x_max):
    canvas = ROOT.TCanvas("c")
    canvas.cd()
    hist.Draw()
    hist.SetLineColor( color[1])
    hist.SetLineWidth(2)
    hist.SetTitle(";"+x_label+"; Events")
    hist.GetYaxis().SetTitleOffset(1.15)
    #hist.SetMinimum(0.9*min(hist.GetMinimum(),hist.GetMinimum()))
    hist.SetMinimum(0.1)
    hist.SetMaximum(1.1*max(hist.GetMaximum(),hist.GetMaximum()))
    # hist.SetAxisRange(x_min,x_max, "X")
    # hist.SetNdivisions(x_div)

    posleg_("R","M",2)

    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0) # 1 for border exist 0 for non
    legend.SetHeader("#kappa_{#lambda}=1","C")
    legend.AddEntry(hist, " ("+str(int(hist.GetEntries()))+")")
    legend.Draw("same")
    canvas.Update()
    canvas.Print("mHH_1.png")
    canvas.Close()
    return hist


if __name__ == "__main__" :
    print("Hello, Start Plotting for Emulation study")
    emulation_passed_taus_pt("kl10.root", 3)

    # main(sys.argv[1])