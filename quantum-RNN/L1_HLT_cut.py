# Author: Shiwen An 
# Date: 2022.05.30
# Purpose: Adding L1 and HLT Cut

from sympy import true
from HLT_Study import *

# Comments line by line
# leg = TLegend(.73,.32,.97,.53) # TLegend(x1,y1,x2,y2) where x,y are in units of percentage of canvas (i.e. x,y \in [0,1])
# leg.SetBorderSize(0) # no border
# leg.SetFillColor(0) # probably kWhite
# leg.SetFillStyle(0) # I'm guessing this just means pure color, no patterns 
# leg.SetTextFont(42)
# leg.SetTextSize(0.035) # somewhat large, may need to play with this to make the plot look ok
# leg.AddEntry(g1,"2X_{n}","L") # AddEntry(TGraph/TH1D varName, what you want the legend to say for this graph, show the line)
# leg.AddEntry(geq1,"2X_{n,eq}","L")
# leg.Draw() # draw it!
# leg = TLegend(.73,.32,.97,.53)
# leg.SetBorderSize(0)
# leg.SetFillColor(0)
# leg.SetFillStyle(0)
# leg.SetTextFont(42)
# leg.SetTextSize(0.035)
# leg.AddEntry(g1,"2X_{n}","L")
# leg.AddEntry(geq1,"2X_{n,eq}","L")
# leg.Draw()


taus = ["r22_Pass", "r22_PassFail", "Tau0_Pass", "Tau0_PassFail"]
list_order = [
        "RNN Score",
        "Prong",
        "#Delta R",
        "p_{T}^{#tau} leading",
        "p_{T}^{#tau} Subleading"
]

def ratio_tree_loop_cut_pt( input_root, t ):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open( input_root ,"READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltpt = []
    hlteta = []
    L1 = "N/A"
    HLT = "N/A"
###################################################################################
#TrigMatched_Taus_HLTptfl##########################################################

    hist_onhltptrnn = ROOT.TH1D("onhltpt_rnn","",50,0,1)
    hist_onhltptprong = ROOT.TH1D("onhltpt_prong","",10,0,10)
    hist_onhltptpt_r = ROOT.TH1D("onhltptpt_r","",50,0,50)
    hist_onhltptpt_lead_r = ROOT.TH1D("onhltptpt_lead_r","",50,0,50)
    hist_onhltptpt_sublead_r = ROOT.TH1D("onhltptpt_sublead_r","",50,0,50)
    hist_onhltptdeltaR = ROOT.TH1D("onhltptdeltaR", "",50, -1, 4)

    hist_L1_onhltptrnn = ROOT.TH1D("L1_onhltpt_rnn","",50,0,1)
    hist_L1_onhltptprong = ROOT.TH1D("L1_onhltpt_prong","",10,0,10)
    hist_L1_onhltptpt_r = ROOT.TH1D("L1_onhltptpt_r","",50,0,50)
    hist_L1_onhltptpt_lead_r = ROOT.TH1D("L1_onhltptpt_lead_r","",50,0,50)
    hist_L1_onhltptpt_sublead_r = ROOT.TH1D("L1_onhltptpt_sublead_r","",50,0,50)
    hist_L1_onhltptdeltaR = ROOT.TH1D("L1_onhltptdeltaR", "",50, -1, 4)

    hist_HLT_onhltptrnn = ROOT.TH1D("HLT_onhltpt_rnn","",50,0,1)
    hist_HLT_onhltptprong = ROOT.TH1D("HLT_onhltpt_prong","",10,0,10)
    hist_HLT_onhltptpt_r = ROOT.TH1D("HLT_onhltptpt_r","",50,0,50)
    hist_HLT_onhltptpt_lead_r = ROOT.TH1D("HLT_onhltptpt_lead_r","",100,0,500)
    hist_HLT_onhltptpt_sublead_r = ROOT.TH1D("HLT_onhltptpt_sublead_r","",100,0,500)
    hist_HLT_onhltptdeltaR = ROOT.TH1D("HLT_onhltptdeltaR", "",50, -1, 4)

    # Manual Cut add later if necessary
    hist_m_onhltptrnn = ROOT.TH1D("m_onhltpt_rnn","",50,0,1)
    hist_m_onhltptprong = ROOT.TH1D("m_onhltpt_prong","",10,0,10)
    hist_m_onhltptpt_lead_r = ROOT.TH1D("m_onhltptpt_lead_r","",100,0,500)
    hist_m_onhltptpt_sublead_r = ROOT.TH1D("m_onhltptpt_sublead_r","",100,0,500)
    hist_m_onhltptdeltaR = ROOT.TH1D("m_onhltptdeltaR", "",50, -1, 4)

    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        L1_1 = getattr(tree, "L1_J25")
        L1 = "L1_J25"
        # Bit confused about this point of trigger use 
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "r22_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "Tau0_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J20_Tau0"
        elif taus[t] == "Tau0_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J20_Tau0"

        # Loop over without cut 
        for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
            hist_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
            if(i==0):  
                hist_onhltptpt_lead_r.Fill(
                    tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
            if(i==1):
                hist_onhltptpt_sublead_r.Fill(
                    tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                hist_onhltptdeltaR.Fill(vec1.DeltaR(vec0))  
            
            # Manual Cut Addition
            # if(i==0 and tree.TrigMatched_Taus_HLTptfl[i].Pt()>35):
            #     hist_m_onhltptpt_lead_r.Fill(
            #         tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
            # if(i==1 and tree.TrigMatched_Taus_HLTptfl[i].Pt()>25):
            #     hist_m_onhltptpt_sublead_r.Fill(
            #         tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)  

        for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
            hist_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
        for k in range(len(tree.TrigMatched_prong_HLTptfl)):
            hist_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)

        # Loop over with L1 cut 
        if L1_1:
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                hist_L1_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                if(i==0):
                    hist_L1_onhltptpt_lead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                if(i==1):
                    hist_L1_onhltptpt_sublead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                    # Fill DeltaR
                    vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                    vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                    hist_L1_onhltptdeltaR.Fill(vec0.DeltaR(vec1))
                if(i==0 and tree.TrigMatched_Taus_HLTptfl[i].Pt()>35):
                    hist_m_onhltptpt_lead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                if(i==1 and tree.TrigMatched_Taus_HLTptfl[i].Pt()>25):
                    hist_m_onhltptpt_sublead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[1].Pt(),1) 
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                hist_L1_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
            for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                hist_L1_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)
            # Loop over with HLT cut 
            if HLT_1:
                for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                    hist_HLT_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                    if(i==0):
                        hist_HLT_onhltptpt_lead_r.Fill(tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                    if(i==1):
                        hist_HLT_onhltptpt_sublead_r.Fill(tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                        # Fill DeltaR
                        vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                        vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                        hist_HLT_onhltptdeltaR.Fill(vec0.DeltaR(vec1))
                for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_HLT_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
                for k in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_HLT_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)
    
    hltpt.append(hist_onhltptrnn)
    hltpt.append(hist_onhltptprong)
    hltpt.append(hist_onhltptdeltaR)
    hltpt.append(hist_onhltptpt_lead_r)
    hltpt.append(hist_onhltptpt_sublead_r)

    hltpt.append(hist_L1_onhltptrnn)
    hltpt.append(hist_L1_onhltptprong)
    hltpt.append(hist_L1_onhltptdeltaR)
    hltpt.append(hist_L1_onhltptpt_lead_r)
    hltpt.append(hist_L1_onhltptpt_sublead_r)

    hltpt.append(hist_HLT_onhltptrnn)
    hltpt.append(hist_HLT_onhltptprong)
    hltpt.append(hist_HLT_onhltptdeltaR)
    hltpt.append(hist_HLT_onhltptpt_lead_r)
    hltpt.append(hist_HLT_onhltptpt_sublead_r)

######################################################################################

    hlt_ratio = []
    hlt_ratio.append(hist_HLT_onhltptpt_lead_r)
    hlt_ratio.append(hist_HLT_onhltptpt_sublead_r)
    hlt_ratio.append(hist_m_onhltptpt_lead_r)
    hlt_ratio.append(hist_m_onhltptpt_sublead_r)  

    for i in range(2):
        hist_print_compare([hlt_ratio[i],
                            hlt_ratio[i+2]],
                ["HLT_r22", "L1+Manual"],
                list_order[i+3], t)


# Task one: Compare the manual cut with the 
# Trigger cut. 

def tree_loop_cut_pt( input_root, t ):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open( input_root ,"READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltpt = []
    hlteta = []
    L1 = "N/A"
    HLT = "N/A"
###################################################################################
#TrigMatched_Taus_HLTptfl##########################################################

    hist_onhltptrnn = ROOT.TH1D("onhltpt_rnn","",50,0,1)
    hist_onhltptprong = ROOT.TH1D("onhltpt_prong","",10,0,10)
    hist_onhltptpt_r = ROOT.TH1D("onhltptpt_r","",50,0,50)
    hist_onhltptpt_lead_r = ROOT.TH1D("onhltptpt_lead_r","",50,0,50)
    hist_onhltptpt_sublead_r = ROOT.TH1D("onhltptpt_sublead_r","",50,0,50)
    hist_onhltptdeltaR = ROOT.TH1D("onhltptdeltaR", "",50, -1, 4)

    hist_L1_onhltptrnn = ROOT.TH1D("L1_onhltpt_rnn","",50,0,1)
    hist_L1_onhltptprong = ROOT.TH1D("L1_onhltpt_prong","",10,0,10)
    hist_L1_onhltptpt_r = ROOT.TH1D("L1_onhltptpt_r","",50,0,50)
    hist_L1_onhltptpt_lead_r = ROOT.TH1D("L1_onhltptpt_lead_r","",50,0,50)
    hist_L1_onhltptpt_sublead_r = ROOT.TH1D("L1_onhltptpt_sublead_r","",50,0,50)
    hist_L1_onhltptdeltaR = ROOT.TH1D("L1_onhltptdeltaR", "",50, -1, 4)

    hist_HLT_onhltptrnn = ROOT.TH1D("HLT_onhltpt_rnn","",50,0,1)
    hist_HLT_onhltptprong = ROOT.TH1D("HLT_onhltpt_prong","",10,0,10)
    hist_HLT_onhltptpt_r = ROOT.TH1D("HLT_onhltptpt_r","",50,0,50)
    hist_HLT_onhltptpt_lead_r = ROOT.TH1D("HLT_onhltptpt_lead_r","",50,0,50)
    hist_HLT_onhltptpt_sublead_r = ROOT.TH1D("HLT_onhltptpt_sublead_r","",50,0,50)
    hist_HLT_onhltptdeltaR = ROOT.TH1D("HLT_onhltptdeltaR", "",50, -1, 4)

    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        L1_1 = getattr(tree, "L1_J25")
        L1 = "L1_J25"
        # Bit confused about this point of trigger use 
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "r22_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT = "HLT_J25_r22"
        elif taus[t] == "Tau0_Pass":
            HLT_1 = getattr(tree, "HLT_J25_Tau0")
            HLT = "HLT_J20_Tau0"
        elif taus[t] == "Tau0_PassFail":
            HLT_1 = getattr(tree, "HLT_J25_Tau0")
            HLT = "HLT_J20_Tau0"

        # Loop over without cut 
        for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
            hist_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
            if(i==0):  
                hist_onhltptpt_lead_r.Fill(
                    tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
            if(i==1):
                hist_onhltptpt_sublead_r.Fill(
                    tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                hist_onhltptdeltaR.Fill(vec1.DeltaR(vec0))  
        for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
            hist_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
        for k in range(len(tree.TrigMatched_rnn_HLTptfl)):
            hist_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)

        # Loop over with L1 cut 
        if L1_1:
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                hist_L1_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                if(i==0 and tree.TrigMatched_Taus_HLTptfl[0].Pt()>35):
                    hist_L1_onhltptpt_lead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                if(i==1 and tree.TrigMatched_Taus_HLTptfl[1].Pt()>25):
                    hist_L1_onhltptpt_sublead_r.Fill(
                        tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                    # Fill DeltaR
                    vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                    vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                    hist_L1_onhltptdeltaR.Fill(vec0.DeltaR(vec1))
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                hist_L1_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
            for k in range(len(tree.TrigMatched_rnn_HLTptfl)):
                hist_L1_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)
            # Loop over with HLT cut 
            if HLT_1:
                for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                    hist_HLT_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                    if(i==0 and tree.TrigMatched_Taus_HLTptfl[0].Pt()>35):
                        hist_HLT_onhltptpt_lead_r.Fill(tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                    if(i==1 and tree.TrigMatched_Taus_HLTptfl[1].Pt()>25):
                        hist_HLT_onhltptpt_sublead_r.Fill(tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                        # Fill DeltaR
                        vec0= tree.TrigMatched_Taus_HLTptfl[0].Vect()
                        vec1= tree.TrigMatched_Taus_HLTptfl[1].Vect()
                        hist_HLT_onhltptdeltaR.Fill(vec0.DeltaR(vec1))
                for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_HLT_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
                for k in range(len(tree.TrigMatched_rnn_HLTptfl)):
                    hist_HLT_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)
    
    hltpt.append(hist_onhltptrnn)
    hltpt.append(hist_onhltptprong)
    hltpt.append(hist_onhltptdeltaR)
    hltpt.append(hist_onhltptpt_lead_r)
    hltpt.append(hist_onhltptpt_sublead_r)

    hltpt.append(hist_L1_onhltptrnn)
    hltpt.append(hist_L1_onhltptprong)
    hltpt.append(hist_L1_onhltptdeltaR)
    hltpt.append(hist_L1_onhltptpt_lead_r)
    hltpt.append(hist_L1_onhltptpt_sublead_r)

    hltpt.append(hist_HLT_onhltptrnn)
    hltpt.append(hist_HLT_onhltptprong)
    hltpt.append(hist_HLT_onhltptdeltaR)
    hltpt.append(hist_HLT_onhltptpt_lead_r)
    hltpt.append(hist_HLT_onhltptpt_sublead_r)

######################################################################################

    for i in range(5):
        #posleg(leg_pos[i][0], leg_pos[i][1], leg_pos[i][2])
        hist_print_compare([hltpt[i],
                            hltpt[i+5], 
                            hltpt[i+10]],
                ["N/A", L1,  HLT],
                list_order[i], t)
        a = [   int(hltpt[i].GetEntries()), 
                int(hltpt[i+5].GetEntries()), 
                int(hltpt[i+10].GetEntries())]
        print("Efficiency HLT/L1", a[2]/a[1])
        b = [   hltpt[i].GetName(), 
                hltpt[i+5].GetName(), 
                hltpt[i+10].GetName()]
        print("Efficiency "+b[2]+"HLT/L1", a[2]/a[1])

def tree_loop_cut_eta( input_root, t ):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open( input_root ,"READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltpt = []
    hlteta = []
    L1 = "N/A"
    HLT = "N/A"

###TrigMatched_Taus_HLTetafl##################################################################################
    hist_onhltetarnn = ROOT.TH1D("onhlteta_rnn","",50,0,1)
    hist_onhltetaprong = ROOT.TH1D("onhlteta_prong","",10,0,10)
    hist_onhltetapt_r = ROOT.TH1D("onhltetapt_r","",50,0,50)
    hist_onhltetapt_lead_r = ROOT.TH1D("onhltetapt_lead_r","",50,0,50)
    hist_onhltetapt_sublead_r = ROOT.TH1D("onhltetapt_sublead_r","",50,0,50)
    hist_onhltetadeltaR = ROOT.TH1D("onhltetadeltaR", "",50, -1, 4)
    
    hist_L1_onhltetarnn = ROOT.TH1D("L1_onhlteta_rnn","",50,0,1)
    hist_L1_onhltetaprong = ROOT.TH1D("L1_onhlteta_prong","",10,0,10)
    hist_L1_onhltetapt_r = ROOT.TH1D("L1_onhltetapt_r","",50,0,50)
    hist_L1_onhltetapt_lead_r = ROOT.TH1D("L1_onhltetapt_lead_r","",50,0,50)
    hist_L1_onhltetapt_sublead_r = ROOT.TH1D("L1_onhltetapt_sublead_r","",50,0,50)
    hist_L1_onhltetadeltaR = ROOT.TH1D("L1_onhltetadeltaR", "",50, -1, 4)

    hist_HLT_onhltetarnn = ROOT.TH1D("HLT_onhlteta_rnn","",50,0,1)
    hist_HLT_onhltetaprong = ROOT.TH1D("HLT_onhlteta_prong","",10,0,10)
    hist_HLT_onhltetapt_r = ROOT.TH1D("HLT_onhltetapt_r","",50,0,50)
    hist_HLT_onhltetapt_lead_r = ROOT.TH1D("HLT_onhltetapt_lead_r","",50,0,50)
    hist_HLT_onhltetapt_sublead_r = ROOT.TH1D("HLT_onhltetapt_sublead_r","",50,0,50)
    hist_HLT_onhltetadeltaR = ROOT.TH1D("HLT_onhltetadeltaR", "",50, -1, 4)

    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        L1_2 = getattr(tree, "L1_ETA25")
        L1 = "L1_ETA25"
        # Bit confused about this point of trigger use 
        if taus[t] == "r22_Pass":
            HLT_2 = getattr(tree, "HLT_ETA25_r22")
            HLT = "HLT_ETA25_r22"
        elif taus[t] == "r22_PassFail":
            HLT_2 = getattr(tree, "HLT_ETA25_r22")
            HLT = "HLT_ETA25_r22"
        elif taus[t] == "Tau0_Pass":
            HLT_2 = getattr(tree, "HLT_ETA25_Tau0")
            HLT = "HLT_ETA25_Tau0"
        elif taus[t] == "Tau0_PassFail":
            HLT_2 = getattr(tree, "HLT_ETA25_Tau0")
            HLT = "HLT_ETA25_Tau0"

        for i in range(len(tree.TrigMatched_Taus_HLTetafl)):
            hist_onhltetapt_r.Fill(tree.TrigMatched_Taus_HLTetafl[i].Pt(),1)
            if(i==0):
                hist_onhltetapt_lead_r.Fill(
                    tree.TrigMatched_Taus_HLTetafl[0].Pt(),1)
            if(i==1):
                hist_onhltetapt_sublead_r.Fill(
                    tree.TrigMatched_Taus_HLTetafl[1].Pt(),1)
                vec0= tree.TrigMatched_Taus_HLTetafl[0].Vect()
                vec1= tree.TrigMatched_Taus_HLTetafl[1].Vect()
                hist_onhltetadeltaR.Fill(vec1.DeltaR(vec0))  
        for j in range(len(tree.TrigMatched_rnn_HLTetafl)):
            hist_onhltetarnn.Fill(tree.TrigMatched_rnn_HLTetafl[j],1)
        for k in range(len(tree.TrigMatched_rnn_HLTetafl)):
            hist_onhltetaprong.Fill(tree.TrigMatched_prong_HLTetafl[k], 1)

        if L1_2:
            for i in range(len(tree.TrigMatched_Taus_HLTetafl)):
                hist_L1_onhltetapt_r.Fill(tree.TrigMatched_Taus_HLTetafl[i].Pt(),1)
                if(i==0):
                    hist_L1_onhltetapt_lead_r.Fill(
                        tree.TrigMatched_Taus_HLTetafl[0].Pt(),1)
                if(i==1):
                    hist_L1_onhltetapt_sublead_r.Fill(
                        tree.TrigMatched_Taus_HLTetafl[1].Pt(),1)
                    vec0= tree.TrigMatched_Taus_HLTetafl[0].Vect()
                    vec1= tree.TrigMatched_Taus_HLTetafl[1].Vect()
                    hist_L1_onhltetadeltaR.Fill(vec1.DeltaR(vec0))  
            for j in range(len(tree.TrigMatched_rnn_HLTetafl)):
                hist_L1_onhltetarnn.Fill(tree.TrigMatched_rnn_HLTetafl[j],1)
            for k in range(len(tree.TrigMatched_rnn_HLTetafl)):
                hist_L1_onhltetaprong.Fill(tree.TrigMatched_prong_HLTetafl[k], 1)
            if HLT_2:
                for i in range(len(tree.TrigMatched_Taus_HLTetafl)):
                    hist_HLT_onhltetapt_r.Fill(tree.TrigMatched_Taus_HLTetafl[i].Pt(),1)
                    if(i==0):
                        hist_HLT_onhltetapt_lead_r.Fill(
                            tree.TrigMatched_Taus_HLTetafl[0].Pt(),1)
                    if(i==1):
                        hist_HLT_onhltetapt_sublead_r.Fill(
                            tree.TrigMatched_Taus_HLTetafl[1].Pt(),1)
                        vec0= tree.TrigMatched_Taus_HLTetafl[0].Vect()
                        vec1= tree.TrigMatched_Taus_HLTetafl[1].Vect()
                        hist_HLT_onhltetadeltaR.Fill(vec1.DeltaR(vec0))  
                for j in range(len(tree.TrigMatched_rnn_HLTetafl)):
                    hist_HLT_onhltetarnn.Fill(tree.TrigMatched_rnn_HLTetafl[j],1)
                for k in range(len(tree.TrigMatched_rnn_HLTetafl)):
                    hist_HLT_onhltetaprong.Fill(tree.TrigMatched_prong_HLTetafl[k], 1)

    hlteta.append(hist_onhltetarnn)
    hlteta.append(hist_onhltetaprong)
    hlteta.append(hist_onhltetadeltaR)
    hlteta.append(hist_onhltetapt_lead_r)
    hlteta.append(hist_onhltetapt_sublead_r)

    hlteta.append(hist_L1_onhltetarnn)
    hlteta.append(hist_L1_onhltetaprong)
    hlteta.append(hist_L1_onhltetadeltaR)
    hlteta.append(hist_L1_onhltetapt_lead_r)
    hlteta.append(hist_L1_onhltetapt_sublead_r)

    hlteta.append(hist_HLT_onhltetarnn)
    hlteta.append(hist_HLT_onhltetaprong)
    hlteta.append(hist_HLT_onhltetadeltaR)
    hlteta.append(hist_HLT_onhltetapt_lead_r)
    hlteta.append(hist_HLT_onhltetapt_sublead_r)
######################################################################################
    for i in range(5):
        posleg(leg_pos[i][0], leg_pos[i][1], leg_pos[i][2])
        hist_print_compare([hlteta[i],
                            hlteta[i+5], 
                            hlteta[i+10]],
                ["N/A", L1,  HLT],
                list_order[i], t)
        a = [   int(hlteta[i].GetEntries()), 
                int(hlteta[i+5].GetEntries()), 
                int(hlteta[i+10].GetEntries())]
        b = [   hlteta[i].GetName(), 
                hlteta[i+5].GetName(), 
                hlteta[i+10].GetName()]
        print("Efficiency "+b[2]+"HLT/L1", a[2]/a[1])

def main():
    # ratio_tree_loop_cut_pt( "r22_PassFail.root", 1)
    # ratio_tree_loop_cut_pt( "Tau0_PassFail.root", 3)
    # ratio_tree_loop_cut_pt( "Tau0_Pass.root", 2)

    tree_loop_cut_pt( "r22_Pass.root", 0)
    # tree_loop_cut("r22_PassFail.root", 1)
    # tree_loop_cut_pt("Tau0_PassFail.root", 3)
    # tree_loop_cut_pt("Tau0_Pass.root", 2)
    # tree_loop_cut_eta("Tau0_Pass.root", 2)

if __name__ == "__main__" :
    print("Hello, Start Ploting for HLT")
    main()

# 2022/06/06 Comment on such study
# 1. The deltaR, why does it has double 
#    peak for leading and subleading
#   using the includeFailed information 
#   and why does it accumulate around 
# 2. Why does it have some cut for 
#   leading and subleading pt which 
#   could not observe in the plots 
#   by other person. 

# 2022/06/15 Comment
# compare Tau0 r22 on 