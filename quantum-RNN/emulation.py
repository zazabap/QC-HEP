# Author: Shiwen An 
# Date: 2022/06/28 
# Purpose: Add some code for emulation
# Emulate the Normal Trigger with the 

import sys
from xmlrpc.client import Fault
from sympy import false, true
from torch import log2_
from HLT_Study import *
from L1_HLT_cut import *

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

def rnn_region(pt0,pt1,rnn_m_0, rnn_m_1, rnn_l_0, rnn_l_1):
    passPtRNN = false
    if(pt0<=280 and pt1<=280): passPtRNN = rnn_m_0 and rnn_m_1 
    if(pt0<=280 and pt1>280 and pt1<=440): passPtRNN = rnn_m_0 and rnn_l_1
    if(pt0>280 and pt0<=440 and pt1<=280): passPtRNN = rnn_l_0 and rnn_m_1
    if(pt0>280 and pt0<=440 and pt1>280 and pt1<=440): passPtRNN = rnn_l_0 and rnn_l_1
    if(pt0<=280 and pt1>440): passPtRNN = rnn_m_0 
    if(pt0>440 and pt1<=280): passPtRNN = rnn_m_1 
    if(pt0>440 and pt1>280 and pt1<=440): passPtRNN = rnn_l_1
    if(pt0>280 and pt0<=440 and pt1>440): passPtRNN = rnn_l_0   
    if(pt0>440 and pt1>440): passPtRNN = true
    return passPtRNN

def tree_online_RNN(tree):
    passRNN = false

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
            if (rnn): passRNN = true
    return passRNN

def tree_online_RNNdR(tree):
    passRNNdR = false
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
            if (rnn == true ): 
                dR = vec0.DeltaR(vec1)
                if ( dR> 0.3 and dR <3.0) : passRNNdR = true            
    return passRNNdR

def tree_online_dR(tree):
    passdR = false
    for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
        for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if (i==j): continue
            vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
            vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
            dR = vec0.DeltaR(vec1)
            if ( dR> 0.3 and dR <3.0) : passdR = true            
    return passdR

def tree_online_PtRNNdR(tree, emu):
    passPt = false
    passPtdR = false
    passRNN = false
    passPtRNN = false
    passPtRNNdR = false

    if(emu == 0): 
        for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
            for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
                if (i==j): continue
                if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
                passPt = true
    
    if(emu == 1):
        for i in range(len(tree.TrigMatched_Taus_HLTptfl)) :
            if ( tree.TrigMatched_Taus_HLTptfl[i].Pt() < 35): continue
            for  j in range(len(tree.TrigMatched_Taus_HLTptfl)) :
                if (i==j): continue
                if ( tree.TrigMatched_Taus_HLTptfl[j].Pt() < 25): continue
                vec0 = tree.TrigMatched_Taus_HLTptfl[j].Vect()
                vec1 = tree.TrigMatched_Taus_HLTptfl[i].Vect()
                dR = vec0.DeltaR(vec1)
                if (  dR> 0.3 and dR <3.0) : 
                    passPtdR = true

    if(emu == 2):
        for i in range(len(tree.TrigMatched_rnn_HLTptfl)):
            if (tree.TrigMatched_rnn_HLTptfl[i]): passRNN = true


    if(emu == 3):
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

    if(emu == 4):
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
                if (  dR> 0.3 and dR <3.0) : passPtRNNdR = true
    return [passPt,passPtdR,passRNN, passPtRNN, passPtRNNdR] 

def fill_hist_pt(tree, emu):
    entries = range(tree.GetEntries())
    hltoff = []

    hist_m_offhltrnn = ROOT.TH1D("m_offhlt_rnn", "", 50, 0, 1)
    hist_m_offhltprong = ROOT.TH1D("m_offhlt_prong", "", 10, 0, 10)
    hist_m_offhltpt_r = ROOT.TH1D(
        "m_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltpt_lead_r = ROOT.TH1D(
        "m_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltpt_sublead_r = ROOT.TH1D(
        "m_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltptdeltaR = ROOT.TH1D("m_offhltptdeltaR", "", 50, -1, 4)

    hist_HLT_offhltrnn = ROOT.TH1D("HLT_offhlt_rnn", "", 50, 0, 1)
    hist_HLT_offhltprong = ROOT.TH1D("HLT_offhlt_prong", "", 10, 0, 10)
    hist_HLT_offhltpt_r = ROOT.TH1D(
        "HLT_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_lead_r = ROOT.TH1D(
        "HLT_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_sublead_r = ROOT.TH1D(
        "HLT_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltptdeltaR = ROOT.TH1D("HLT_offhltptdeltaR", "", 50, -1, 4)

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
        select = select and (L1_1 or L1_2)

        # How to pass RNN loose ID?
        if(select):
            EMU_1 = tree_online_PtRNNdR(tree, emu)
            if L1_1 and EMU_1[emu]:
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
                            passPtRNNdR = true
                            hist_m_offhltpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[j].Pt())
                            hist_m_offhltpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt())
        
    hist_print_compare([ hist_m_offhltpt_r ], ["Pt"], emu_order[0], 0)


def emulation_stage(input_root, t):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open(input_root, "READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltoff = []
####Off_Matched_Tau##################################################################################
    hist_offhltrnn = ROOT.TH1D("offhlt_rnn", "", 50, 0, 1)
    hist_offhltprong = ROOT.TH1D("offhlt_prong", "", 10, 0, 10)
    hist_offhltpt_r = ROOT.TH1D("offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_lead_r = ROOT.TH1D(
        "offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_sublead_r = ROOT.TH1D(
        "offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltptdeltaR = ROOT.TH1D("offhltptdeltaR", "", 50, -1, 4)

    hist_m1_offhltrnn = ROOT.TH1D("m1_offhlt_rnn", "", 50, 0, 1)
    hist_m1_offhltprong = ROOT.TH1D("m1_offhlt_prong", "", 10, 0, 10)
    hist_m1_offhltpt_r = ROOT.TH1D(
        "m1_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m1_offhltpt_lead_r = ROOT.TH1D(
        "m1_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m1_offhltpt_sublead_r = ROOT.TH1D(
        "m1_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m1_offhltptdeltaR = ROOT.TH1D("m1_offhltptdeltaR", "", 50, -1, 4)

    hist_m2_offhltrnn = ROOT.TH1D("m2_offhlt_rnn", "", 50, 0, 1)
    hist_m2_offhltprong = ROOT.TH1D("m2_offhlt_prong", "", 10, 0, 10)
    hist_m2_offhltpt_r = ROOT.TH1D(
        "m2_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m2_offhltpt_lead_r = ROOT.TH1D(
        "m2_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m2_offhltpt_sublead_r = ROOT.TH1D(
        "m2_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m2_offhltptdeltaR = ROOT.TH1D("m2_offhltptdeltaR", "", 50, -1, 4)

    hist_m3_offhltrnn = ROOT.TH1D("m3_offhlt_rnn", "", 50, 0, 1)
    hist_m3_offhltprong = ROOT.TH1D("m3_offhlt_prong", "", 10, 0, 10)
    hist_m3_offhltpt_r = ROOT.TH1D(
        "m3_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m3_offhltpt_lead_r = ROOT.TH1D(
        "m3_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m3_offhltpt_sublead_r = ROOT.TH1D(
        "m3_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m3_offhltptdeltaR = ROOT.TH1D("m3_offhltptdeltaR", "", 50, -1, 4)


    hist_m4_offhltrnn = ROOT.TH1D("m4_offhlt_rnn", "", 50, 0, 1)
    hist_m4_offhltprong = ROOT.TH1D("m4_offhlt_prong", "", 10, 0, 10)
    hist_m4_offhltpt_r = ROOT.TH1D(
        "m4_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m4_offhltpt_lead_r = ROOT.TH1D(
        "m4_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m4_offhltpt_sublead_r = ROOT.TH1D(
        "m4_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m4_offhltptdeltaR = ROOT.TH1D("m4_offhltptdeltaR", "", 50, -1, 4)


    hist_HLT_offhltrnn = ROOT.TH1D("HLT_offhlt_rnn", "", 50, 0, 1)
    hist_HLT_offhltprong = ROOT.TH1D("HLT_offhlt_prong", "", 10, 0, 10)
    hist_HLT_offhltpt_r = ROOT.TH1D(
        "HLT_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_lead_r = ROOT.TH1D(
        "HLT_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_sublead_r = ROOT.TH1D(
        "HLT_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltptdeltaR = ROOT.TH1D("HLT_offhltptdeltaR", "", 50, -1, 4)

    # Selection+ Selection Pass HLT
    denominator = 0 # entries (pass select + L1)
    numerator_emu = 0 # entries (pass selection + L1) + (emu/HLT [online taus])
    numerator_hlt =0  # entries (pass selection + L1) + (emu/HLT [online taus])

    numerator_1 = 0 # pt
    numerator_2 = 0 # ptdR
    numerator_3 = 0 # ptRNN
    numerator_4 = 0 # ptRNNdR

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
        select = select and (L1_1 or L1_2)

        # How to pass RNN loose ID?
        if(select):
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                hist_offhltpt_r.Fill(pt0, 1)
                if(i == 0):
                    hist_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                if(i == 1):
                    hist_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                    vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                    vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                    hist_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
            for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                    hist_offhltprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)  
            if L1_1: denominator = denominator+1
            if L1_1:
                EMU_1 = tree_online_PtRNNdR(tree, 0)
                if EMU_1[0]:
                    numerator_1 = numerator_1 +1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_m1_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_m1_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_m1_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_m1_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_m1_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_m1_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)  
                EMU_1 = tree_online_PtRNNdR(tree, 1)
                if EMU_1[1]:
                    numerator_2 = numerator_2 + 1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_m2_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_m2_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_m2_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_m2_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_m2_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_m2_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)  
                EMU_1 = tree_online_PtRNNdR(tree, 3)
                if EMU_1[3]:
                    numerator_3 = numerator_3 + 1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_m3_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_m3_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_m3_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_m3_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_m3_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_m3_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)  
                EMU_1 = tree_online_PtRNNdR(tree, 4)
                if EMU_1[4]:
                    numerator_4 = numerator_4 + 1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_m4_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_m4_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_m4_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_m4_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_m4_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_m4_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)  

    print("Event level check")
    print("pt: ", numerator_1, "percentage: ", numerator_1/denominator )
    print("ptdR: ", numerator_2, "percentage: ", numerator_2/denominator)
    print("ptRNN: ", numerator_3, "percentage: ", numerator_3/denominator)
    print("ptRNNdR: ", numerator_4, "percentage: ", numerator_4/denominator)
    print("select: ", denominator)


    hltoff.append(hist_offhltrnn)
    hltoff.append(hist_offhltprong)
    hltoff.append(hist_offhltptdeltaR)
    hltoff.append(hist_offhltpt_r)
    hltoff.append(hist_offhltpt_sublead_r)

    # pT
    hltoff.append(hist_m1_offhltrnn)
    hltoff.append(hist_m1_offhltprong)
    hltoff.append(hist_m1_offhltptdeltaR)
    hltoff.append(hist_m1_offhltpt_r)
    hltoff.append(hist_m1_offhltpt_sublead_r)

    # pTdR
    hltoff.append(hist_m2_offhltrnn)
    hltoff.append(hist_m2_offhltprong)
    hltoff.append(hist_m2_offhltptdeltaR)
    hltoff.append(hist_m2_offhltpt_r)
    hltoff.append(hist_m2_offhltpt_sublead_r)

    # pTRNN
    hltoff.append(hist_m3_offhltrnn)
    hltoff.append(hist_m3_offhltprong)
    hltoff.append(hist_m3_offhltptdeltaR)
    hltoff.append(hist_m3_offhltpt_r)
    hltoff.append(hist_m3_offhltpt_sublead_r)

    # pTRNNdR
    hltoff.append(hist_m4_offhltrnn)
    hltoff.append(hist_m4_offhltprong)
    hltoff.append(hist_m4_offhltptdeltaR)
    hltoff.append(hist_m4_offhltpt_r)
    hltoff.append(hist_m4_offhltpt_sublead_r)


    for i in range(5):
        hist_print_compare([hltoff[i],hltoff[i+5],hltoff[i+10], hltoff[i+15], hltoff[i+20]],
            ["select", "pt", "ptdR", "ptRNN", "ptRNNdR"],
            list_order[i], t)    
    
    # hist_print_compare_ratio([hltoff[13], hltoff[3]],
    # ["ptdR", "select"], "p_T", t)

    # hist_print_compare_ratio([hltoff[18], hltoff[3]],
    # ["ptRNN", "select"], "p_T", t)
    
    # hist_print_compare_ratio([hltoff[23], hltoff[3]],
    # ["ptRNNdR", "select"], "p_T", t)

    hist_print_compare_ratio([hltoff[18], hltoff[13]],
    ["ptRNN", "ptdR"], "p_T", t)



def emulation_stage_number(input_root, t):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open(input_root, "READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())


    # Selection+ Selection Pass HLT
    denominator = 0 # entries (pass select + L1)
    numerator_emu = 0 # entries (pass selection + L1) + (emu/HLT [online taus])
    numerator_hlt =0  # entries (pass selection + L1) + (emu/HLT [online taus])

    numerator_1 = 0 # pt
    numerator_2 = 0 # ptdR
    numerator_3 = 0 # ptRNN
    numerator_4 = 0 # ptRNNdR
    numerator_5 = 0 # RNN only
    numerator_6 = 0 # RNNdR 
    numerator_7 = 0 # dR

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
        select = select and (L1_1 or L1_2)

        # How to pass RNN loose ID?
        if(select): 
            if L1_1: denominator = denominator+1
            if L1_1:
                EMU_1 = tree_online_PtRNNdR(tree, 0)
                if EMU_1[0]:
                    numerator_1 = numerator_1 +1
                EMU_1 = tree_online_PtRNNdR(tree, 1)
                if EMU_1[1]:
                    numerator_2 = numerator_2 + 1
                EMU_1 = tree_online_PtRNNdR(tree, 3)
                if EMU_1[3]:
                    numerator_3 = numerator_3 + 1
                EMU_1 = tree_online_PtRNNdR(tree, 4)
                if EMU_1[4]:
                    numerator_4 = numerator_4 + 1
                if tree_online_RNN(tree):
                    numerator_5 = numerator_5 +1
                if tree_online_RNNdR(tree):
                    numerator_6 = numerator_6 +1
                if tree_online_dR(tree):
                    numerator_7 = numerator_7 +1

    print("Event level check")
    print("pt: ", numerator_1, "percentage: ", numerator_1/denominator )
    print("dR: ", numerator_7, "percentage: ", numerator_7/denominator)
    print("RNN: ", numerator_5, "percentage: ", numerator_5/denominator)
    print("ptdR: ", numerator_2, "percentage: ", numerator_2/denominator)
    print("ptRNN: ", numerator_3, "percentage: ", numerator_3/denominator)
    print("RNN dR: ", numerator_6, "percentage: ", numerator_6/denominator)
    print("ptRNNdR: ", numerator_4, "percentage: ", numerator_4/denominator)
    print("select: ", denominator)


def emulation(input_root, t, emu):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open(input_root, "READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltoff = []
####Off_Matched_Tau##################################################################################
    hist_offhltrnn = ROOT.TH1D("offhlt_rnn", "", 50, 0, 1)
    hist_offhltprong = ROOT.TH1D("offhlt_prong", "", 10, 0, 10)
    hist_offhltpt_r = ROOT.TH1D("offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_lead_r = ROOT.TH1D(
        "offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_sublead_r = ROOT.TH1D(
        "offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltptdeltaR = ROOT.TH1D("offhltptdeltaR", "", 50, -1, 4)

    hist_m_offhltrnn = ROOT.TH1D("m_offhlt_rnn", "", 50, 0, 1)
    hist_m_offhltprong = ROOT.TH1D("m_offhlt_prong", "", 10, 0, 10)
    hist_m_offhltpt_r = ROOT.TH1D(
        "m_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltpt_lead_r = ROOT.TH1D(
        "m_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltpt_sublead_r = ROOT.TH1D(
        "m_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_m_offhltptdeltaR = ROOT.TH1D("m_offhltptdeltaR", "", 50, -1, 4)

    hist_HLT_offhltrnn = ROOT.TH1D("HLT_offhlt_rnn", "", 50, 0, 1)
    hist_HLT_offhltprong = ROOT.TH1D("HLT_offhlt_prong", "", 10, 0, 10)
    hist_HLT_offhltpt_r = ROOT.TH1D(
        "HLT_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_lead_r = ROOT.TH1D(
        "HLT_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_sublead_r = ROOT.TH1D(
        "HLT_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltptdeltaR = ROOT.TH1D("HLT_offhltptdeltaR", "", 50, -1, 4)

    # Selection+ Selection Pass HLT
    denominator = 0 # entries (pass select + L1)
    numerator_emu = 0 # entries (pass selection + L1) + (emu/HLT [online taus])
    numerator_hlt =0  # entries (pass selection + L1) + (emu/HLT [online taus])
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
        select = select and (L1_1 or L1_2)

        # How to pass RNN loose ID?
        if(select):
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                hist_offhltpt_r.Fill(pt0, 1)
                if(i == 0):
                    hist_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                if(i == 1):
                    hist_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                    vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                    vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                    hist_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
            for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                    hist_offhltprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)  
            if L1_1: denominator = denominator+1
            EMU_1 = tree_online_PtRNNdR(tree, emu)
            if L1_1:
                if EMU_1[emu]:
                    numerator_emu = numerator_emu+1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_m_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_m_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_m_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_m_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_m_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_m_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)  
            if L1_1 and HLT_1 and tree_online_PtRNNdR(tree,0):
                    numerator_hlt = numerator_hlt+1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_HLT_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_HLT_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_HLT_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_HLT_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_HLT_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_HLT_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)
    
    print("Numerator Emulation",emu_order[emu],":",numerator_emu)
    print("Efficiency Emu:", numerator_emu/denominator)

    hltoff.append(hist_offhltrnn)
    hltoff.append(hist_offhltprong)
    hltoff.append(hist_offhltptdeltaR)
    hltoff.append(hist_offhltpt_r)
    hltoff.append(hist_offhltpt_sublead_r)

    hltoff.append(hist_m_offhltrnn)
    hltoff.append(hist_m_offhltprong)
    hltoff.append(hist_m_offhltptdeltaR)
    hltoff.append(hist_m_offhltpt_r)
    hltoff.append(hist_m_offhltpt_sublead_r)

    hltoff.append(hist_HLT_offhltrnn)
    hltoff.append(hist_HLT_offhltprong)
    hltoff.append(hist_HLT_offhltptdeltaR)
    hltoff.append(hist_HLT_offhltpt_r)
    hltoff.append(hist_HLT_offhltpt_sublead_r)

    for i in range(5):
        hist_print_compare([hltoff[i],hltoff[i+5],hltoff[i+10] ],
            ["select", "emu", "hlt"],
            list_order[i], t)


def HLT(input_root, t):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open(input_root, "READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltoff = []

    hist_offhltrnn = ROOT.TH1D("offhlt_rnn", "", 50, 0, 1)
    hist_offhltprong = ROOT.TH1D("offhlt_prong", "", 10, 0, 10)
    hist_offhltpt_r = ROOT.TH1D("offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_lead_r = ROOT.TH1D(
        "offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltpt_sublead_r = ROOT.TH1D(
        "offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_offhltptdeltaR = ROOT.TH1D("offhltptdeltaR", "", 50, -1, 4)

    hist_HLT_offhltrnn = ROOT.TH1D("HLT_offhlt_rnn", "", 50, 0, 1)
    hist_HLT_offhltprong = ROOT.TH1D("HLT_offhlt_prong", "", 10, 0, 10)
    hist_HLT_offhltpt_r = ROOT.TH1D(
        "HLT_offhltpt_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_lead_r = ROOT.TH1D(
        "HLT_offhltpt_lead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltpt_sublead_r = ROOT.TH1D(
        "HLT_offhltpt_sublead_r", "", r_pt[0], r_pt[1], r_pt[2])
    hist_HLT_offhltptdeltaR = ROOT.TH1D("HLT_offhltptdeltaR", "", 50, -1, 4)
####Off_Matched_Tau##################################################################################

    # Selection+ Selection Pass HLT
    denominator = 0 # entries (pass select + L1)
    numerator_hlt =0  # entries (pass selection + L1) + (emu/HLT [online taus])
    numerator_hlt_check = 0 # entry checks before plot
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
        select = select and (L1_1 or L1_2)

        # How to pass RNN loose ID?
        if(select):
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                hist_offhltpt_r.Fill(pt0, 1)
                if(i == 0):
                    hist_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                if(i == 1):
                    hist_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                    vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                    vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                    hist_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
            for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                    hist_offhltprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)  

            if L1_1: denominator = denominator+1
            if L1_1 and HLT_1:
                if tree_online_PtRNNdR(tree, 0)[0]:
                    numerator_hlt = numerator_hlt+1

            if L1_1 and HLT_1 and tree_online_PtRNNdR(tree,0)[0]:
                    numerator_hlt_check = numerator_hlt_check+1
                    for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                        pt0 = tree.TrigMatched_Taus_HLTptfl[i].Pt()
                        hist_HLT_offhltpt_r.Fill(pt0, 1)
                        if(i == 0):
                            hist_HLT_offhltpt_lead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[0].Pt(), 1)
                        if(i == 1):
                            hist_HLT_offhltpt_sublead_r.Fill(
                                tree.TrigMatched_Taus_HLTptfl[1].Pt(), 1)
                            vec0 = tree.TrigMatched_Taus_HLTptfl[0].Vect()
                            vec1 = tree.TrigMatched_Taus_HLTptfl[1].Vect()
                            hist_HLT_offhltptdeltaR.Fill(vec1.DeltaR(vec0))
                    for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                        hist_HLT_offhltrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j], 1)
                    for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                        hist_HLT_offhltprong.Fill(
                            tree.TrigMatched_prong_HLTptfl[k], 1)
    
    print("Numerator HLT+pt: ", numerator_hlt)
    print("Plot HLT check: ", numerator_hlt_check)
    print("Denominator: ", denominator)
    print("HLT efficiency: ", numerator_hlt/denominator)

    hltoff.append(hist_offhltrnn)
    hltoff.append(hist_offhltprong)
    hltoff.append(hist_offhltptdeltaR)
    hltoff.append(hist_offhltpt_r)
    hltoff.append(hist_offhltpt_sublead_r)

    hltoff.append(hist_HLT_offhltrnn)
    hltoff.append(hist_HLT_offhltprong)
    hltoff.append(hist_HLT_offhltptdeltaR)
    hltoff.append(hist_HLT_offhltpt_r)
    hltoff.append(hist_HLT_offhltpt_sublead_r)

    for i in range(5):
        hist_print_compare([hltoff[i],hltoff[i+5]],
            ["select", "pass hlt"],
            list_order[i], t)


def main(i):
    print(i)
    if (i=="0"): # Emulate pt only
        emulation( "Tau0_PassFail.root", 3 , 0)
    if (i=="1"): # Emulate ptdR only
        emulation( "Tau0_PassFail.root", 3 , 1)
    if (i=="2"): # Delta RNN only
        emulation( "Tau0_PassFail.root", 3 , 2)
    if (i=="3"): # Emulate pt+RNN
        emulation( "Tau0_PassFail.root", 3 , 3)
    if (i=="4"): # Emulate pt+RNN+DeltaR
        # emulation( "Tau0_PassFail.root", 3 , 4)
        # emulation_stage("Tau0_Pass.root", 2)
        emulation_stage("Tau0_PassFail.root", 3)
    
    HLT("Tau0_Pass.root",2)

def test(i):
    emulation_stage_number("Tau0_PassFail.root", 3)


if __name__ == "__main__" :
    print("Hello, Start Ploting for Emulation study")
    test(sys.argv[1])
    # main(sys.argv[1])