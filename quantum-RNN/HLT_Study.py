

# Author: Shiwen An 
# Date: 2022/05/24
# Purpose: Crosscheck 
# More deteailed work 
# with better plots

#!/usr/bin/env python
#Version 22.05.10.11.00
import math
import ROOT
import ast
from ast import Add, BinOp, Num
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("ATLAS")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetErrorX()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetTitleOffset(1.05,"X")
ROOT.gStyle.SetPadLeftMargin(0.125)
ROOT.gStyle.SetPadRightMargin(0.03)
ROOT.gStyle.SetPadTopMargin(0.025)
ROOT.gStyle.SetPadBottomMargin(0.125)
ROOT.gStyle.SetPalette(1)
ROOT.gROOT.ForceStyle()

taus = ["passfail","pass"]
taus = ["r22_Pass", "r22_PassFail", "Tau0_Pass", "Tau0_PassFail"]
color = [ROOT.kViolet,  ROOT.kBlue, ROOT.kGreen,ROOT.kBlack, ROOT.kRed]
kL = [1,10]
kL = [1]
printer = 5000

def posleg(pos_x, pos_y, items):
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

# X_label 
# Canvas Plot Range
# X_min X_max
def hist_print(hist, t, x_label, x_div, x_min, x_max):
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
    hist.SetAxisRange(x_min,x_max, "X")
    hist.SetNdivisions(x_div)

    posleg("R","U",2)

    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0) # 1 for border exist 0 for non
    legend.SetHeader("Higgs","C")
    legend.AddEntry(hist, hist.GetName()+" ("+str(int(hist.GetEntries()))+")")
    legend.Draw("same")
    canvas.Update()
    canvas.Print(hist.GetName()+".png")
    canvas.Close()
    return hist

pos_dR = ["R", "U", 4]
def hist_print_compare_deltaR(hists_onhltn, diffhlt):
    diffsub = ["_{1}", "_{2}"]
    diffpng = ["1", "2"]
    canvas = ROOT.TCanvas("c")
    canvas.cd()
    canvas.SetLogy()
    for h in range(len(hists_onhltn)):
        hists_onhltn[h].Draw("same")
        hists_onhltn[h].SetLineColor( color[h])
        hists_onhltn[h].SetLineWidth(3)
        hists_onhltn[h].SetTitle(";#Delta R; Number of online events")
        hists_onhltn[h].GetYaxis().SetTitleOffset(1.05)
        hists_onhltn[h].SetMinimum(0.1)
        posleg( pos_dR[0], pos_dR[1], pos_dR[2])

    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.SetHeader("#kappa_{#lambda}="+str(kL[0]),"C")
    legend.AddEntry(hists_onhltn[0],"Tau "+diffhlt[0]+" ("+str(int(hists_onhltn[0].GetEntries()))+")")
    legend.AddEntry(hists_onhltn[1],"Tau "+diffhlt[1]+" ("+str(int(hists_onhltn[1].GetEntries()))+")")
    legend.Draw("same")
    canvas.Update()

    canvas.Print(taus[0]+str(kL[0])+"on"+diffhlt[0]+".png")
    canvas.Close()

list_order = [
        "p_{T}^{#tau}", #1
        "p_{T}^{#tau} leading", #2
        "p_{T}^{#tau} Subleading",#3
        "RNN Score",#4
        "Prong",#5
        "p_{T}^{#tau}_r",#6
        "p_{T}^{#tau} leading_r",#7
        "p_{T}^{#tau} Subleading_r",#8
        "pt #Delta R",#9
        "eta #Delta R",#10
        "#Delta R", #11
        "RNN_Score", #12
        "Delta_R", #13
        "leading", #14
        "Subleading", #15
        "leading_eta",  #16
        "Subleading_eta", #17
        "p_T" #18
]

leg_pos =[
        ["R", "D", 4], #1
        ["R", "D", 4], #2
        ["R", "D", 4], #3
        ["C", "D", 4], #4
        ["R", "U", 4], #5
        ["R", "D", 4], #6
        ["R", "D", 4], #7
        ["R", "D", 4], #8
        ["C", "D", 4], #9
        ["C", "D", 4], #10
        ["L", "U", 4], #11
        ["C", "D", 4], #12
        ["L", "U", 4], #13
        ["R", "U", 4], #14
        ["R", "U", 4], #15
        ["C", "D", 4], #16
        ["C", "D", 4], #17
        ["R", "U", 4], #18
]

x_order = [
        "p_{T}^{#tau}", #1
        "p_{T}^{#tau} leading", #2
        "p_{T}^{#tau} Subleading",#3
        "RNN Score",#4
        "Prong",#5
        "p_{T}^{#tau}_r",#6
        "p_{T}^{#tau} leading_r",#7
        "p_{T}^{#tau} Subleading_r",#8
        "pt #Delta R",#9
        "eta #Delta R",#10
        "#Delta R", #11
        "RNN Score", #12
        "#Delta R", #13
        "p_{T}^{#tau} leading", #14
        "p_{T}^{#tau} Subleading",#15
        "#eta leading", #16
        "#eta Subleading",#17
        "p_{T}^{#tau} [GeV]", #18
]

def hist_print_compare(hists_onhltn, diffhlt, x_label, t):
    canvas = ROOT.TCanvas("c")
    canvas.cd()
    i_pos = list_order.index(x_label)
    for h in range(len(hists_onhltn)):
        hists_onhltn[h].Draw("same")
        hists_onhltn[h].SetLineColor( color[h])
        hists_onhltn[h].SetLineWidth(2)
        hists_onhltn[h].SetTitle("; mHH[GeV] ; Number of events")
        hists_onhltn[h].GetYaxis().SetTitleOffset(1.05)
        hists_onhltn[h].SetMinimum(0.1)
    posleg( leg_pos[i_pos][0], leg_pos[i_pos][1], leg_pos[i_pos][2])
    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.SetHeader(" #kappa_{#lambda}=10","C")
    for h in range(len(hists_onhltn)):
        # legend.AddEntry(hists_onhltn[h],"Tau "+diffhlt[h]+" ("+str(int(hists_onhltn[h].GetEntries()))+")")
        legend.AddEntry(hists_onhltn[h], diffhlt[h]+"("+str(int(hists_onhltn[h].GetEntries()))+")")
    legend.Draw("same")
    canvas.Update()
    canvas.Print("mHH_kl1.png")
    canvas.Close()

def createCanvasPads():
    c = ROOT.TCanvas("c", "canvas", 1200, 1200)
    # Upper histogram plot is pad1
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    # pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    #pad2.SetGridy()
    pad2.SetGridy()
    pad2.Draw()
    return c, pad1, pad2

def createRatio(h1, h2, min, max):
    h3 = h1.Clone("h3")
    h3.SetLineColor(ROOT.kBlack)
    h3.SetMarkerStyle(20)
    h3.SetMarkerSize(1)
    h3.SetTitle("")
    h3.SetMinimum(min)
    h3.SetMaximum(max)
    # Set up plot for markers and errors
    # h3.Sumw2()
    # h3.SetStats(0)
    h3.Divide(h2)
 
    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio") 
    y.SetNdivisions(6)
    y.SetTitleSize(40)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.2)
    y.SetLabelFont(43)
    y.SetLabelSize(18)
 
    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(28)
    x.SetTitleFont(43)
    x.SetTitleOffset(1.0)
    x.SetLabelFont(43)
    x.SetLabelSize(25)

    return h3

def hist_print_compare_ratio_eff(hists_onhltn, diffhlt, x_label, t):
    c, pad1, pad2 = createCanvasPads()
    pad1.cd()
    pad1.SetLogy()
    i_pos = list_order.index(x_label)

    if (x_label == "Delta_R"):
        pad1.SetLogy(0)
    
    ymax = 0
    for h in range(len(hists_onhltn)):
        ymax = max(hists_onhltn[h].GetMaximum(),ymax)
    
    for h in range(len(hists_onhltn)):
        hists_onhltn[h].GetYaxis().SetRangeUser(0, ymax*1.1) # Hardcoding
        hists_onhltn[h].Draw("Same")
        hists_onhltn[h].SetLineColor( color[h])
        hists_onhltn[h].SetLineWidth(4)
        hists_onhltn[h].SetTitle("; ; Offline events")
        hists_onhltn[h].GetYaxis().SetTitleOffset(1.05)
        hists_onhltn[h].SetMinimum(0.1)

    pad1.RangeAxis( pad1.GetUxmin(),
    pad1.GetUymin(),
    pad1.GetUxmax(),
    pad1.GetUymax()*1.5 )
    pad1.RedrawAxis()

    posleg( leg_pos[i_pos][0], leg_pos[i_pos][1], leg_pos[i_pos][2])
    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.SetHeader( x_order[i_pos] +" #kappa_{#lambda}="+str(kL[0]),"C")
    for h in range(len(hists_onhltn)):
        legend.AddEntry(hists_onhltn[h], "("+str(int(hists_onhltn[h].GetEntries()))+")"+diffhlt[h])
    legend.Draw("same")
    
    pad1.Update()
    h3 = createRatio(hists_onhltn[1],hists_onhltn[0],0.0,1.05)
    h3.GetYaxis().SetTitle( diffhlt[1]+"/"+diffhlt[0]) 
    x = h3.GetXaxis()
    x.SetTitle(x_order[i_pos])
    pad2.cd()
    h3.Draw("p")

    c.Print(taus[t]+"_"+x_label+".png")
    c.Close()

def hist_print_compare_ratio(hists_onhltn, diffhlt, x_label, t):
    c, pad1, pad2 = createCanvasPads()
    pad1.cd()
    # pad1.SetLogy()
    i_pos = list_order.index(x_label)
    if (x_label == "Delta_R" or 
        x_label == "leading" or 
        x_label == "Subleading"): 
        pad1.SetLogy(0)
    
    # some type of hardcoding
    # Fix the inconsistent y-axis problem
    ymax = 0
    for h in range(len(hists_onhltn)):
        ymax = max(hists_onhltn[h].GetMaximum(),ymax)
    
    for h in range(len(hists_onhltn)):
        hists_onhltn[h].GetYaxis().SetRangeUser(0, ymax*1.1) # Hardcoding
        hists_onhltn[h].Draw("Same")
        hists_onhltn[h].SetLineColor( color[h])
        hists_onhltn[h].SetLineWidth(4)
        hists_onhltn[h].SetTitle("; ; Number of Events")
        hists_onhltn[h].GetYaxis().SetTitleOffset(1.05)
        hists_onhltn[h].SetMinimum(0.1)

    pad1.RangeAxis( pad1.GetUxmin(),
    pad1.GetUymin(),
    pad1.GetUxmax(),
    pad1.GetUymax()*1.5 )
    pad1.RedrawAxis()

    posleg( leg_pos[i_pos][0], leg_pos[i_pos][1], leg_pos[i_pos][2])
    legend = ROOT.TLegend(l_x_min, l_y_min, l_x_max, l_y_max)
    legend.SetTextSize(0.035)
    legend.SetBorderSize(0)
    legend.SetHeader( "#kappa_{#lambda}=10","C")
    for h in range(len(hists_onhltn)):
        legend.AddEntry(hists_onhltn[h], "("+str(int(hists_onhltn[h].GetEntries()))+")"+diffhlt[h])
    legend.Draw("same")
    
    pad1.Update()
    h3 = createRatio(hists_onhltn[0],hists_onhltn[1],0.95, 1.3)
    x = h3.GetXaxis()
    x.SetTitle( "mHH [GeV]")
    pad2.cd()
    h3.Draw("p")

    # c.Print(taus[t]+"_"+x_label+".png")
    c.Print(x_label+".png")
    c.Close()

def hist_efficiency_gain( ):
    print("Done Efficiency Gain")

def tree_loop_deltaR( input_root, t):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open( input_root ,"READ")

    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())

    hist_onhltptdeltaR = ROOT.TH1D("onhltptdeltaR", "",50, -1, 4)
    hist_onhltptdeltaR_lead = ROOT.TH1D("onhltptdeltaR_lead", "",50, -1, 4)
    hist_onhltptdeltaR_sublead = ROOT.TH1D("onhltptdeltaR_sublead", "",50, -1, 4)

    hist_onhltetadeltaR = ROOT.TH1D("onhltetadeltaR", "",50, -1, 4)
    hist_onhltetadeltaR_lead = ROOT.TH1D("onhltetadeltaR_lead", "",50, -1, 4)
    hist_onhltetadeltaR_sublead = ROOT.TH1D("onhltetadeltaR_sublead", "",50, -1, 4)
    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT_1 = getattr(tree, "HLT_ETA25_r22")

        cond_pt = True
        cond_eta = True
        k_on = len(tree.Offline_Matched_Taus)

        if cond_pt:
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                vec= tree.TrigMatched_Taus_HLTptfl[i].Vect()
                for j in range(k_on):
                    hist_onhltptdeltaR.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))
                    if(i==0): 
                        hist_onhltptdeltaR_lead.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))
                    if(i==1): 
                        hist_onhltptdeltaR_sublead.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))

        if cond_eta:
            for i in range(len(tree.TrigMatched_Taus_HLTetafl)):
                vec= tree.TrigMatched_Taus_HLTetafl[i].Vect()
                for j in range(k_on):
                    hist_onhltetadeltaR.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))
                    if(i==0): 
                        hist_onhltetadeltaR_lead.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))
                    if(i==1): 
                        hist_onhltetadeltaR_sublead.Fill(tree.Offline_Matched_Taus[j].Vect().DeltaR(vec))

    diffhlt = ["both","lead", "sublead"]
    hists_onhltn = [ hist_onhltptdeltaR, hist_onhltptdeltaR_lead,hist_onhltptdeltaR_sublead]
    hist_print_compare(hists_onhltn, diffhlt, "pt #Delta R", t)

    diffhlt = ["both","lead", "sublead"]
    hists_onhltn = [ hist_onhltetadeltaR, hist_onhltetadeltaR_lead,hist_onhltetadeltaR_sublead]
    hist_print_compare(hists_onhltn, diffhlt, "eta #Delta R", t)

def tree_loop_hltpt( input_root, t ):
    for k in range(len(kL)):
        if kL[k] == 1:
            inFile = ROOT.TFile.Open( input_root ,"READ")

    print("Start Looping ", taus[t])
    tree = inFile.Get("analysis")
    entries = range(tree.GetEntries())
    hltoff = []
    hltpt = []
    hlteta = []

####Off_Matched_Tau##################################################################################
    hist_offhltpt = ROOT.TH1D("offhltpt","",200,0,1000)
    hist_offhltpt_lead = ROOT.TH1D("offhltpt_lead","",200,0,1000)
    hist_offhltpt_sublead = ROOT.TH1D("offhltpt_sublead","",200,0,1000)
    hist_offhltrnn = ROOT.TH1D("offhlt_rnn","",100,0,1)
    hist_offhltprong = ROOT.TH1D("offhlt_prong","",25,0,25)

    # pt region that are restricted to certain region
    hist_offhltpt_r = ROOT.TH1D("offhltpt_r","",100,0,100)
    hist_offhltpt_lead_r = ROOT.TH1D("offhltpt_lead_r","",100,0,100)
    hist_offhltpt_sublead_r = ROOT.TH1D("offhltpt_sublead_r","",100,0,100)
    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT_1 = getattr(tree, "HLT_ETA25_r22")

        cond_pt = True
        cond_eta = True
        if cond_pt:
            for i in range(len(tree.Offline_Matched_Taus)):
                hist_offhltpt.Fill(tree.Offline_Matched_Taus[i].Pt(),1)
                hist_offhltpt_r.Fill(tree.Offline_Matched_Taus[i].Pt(),1)
                if(i==0): 
                    hist_offhltpt_lead.Fill(tree.Offline_Matched_Taus[0].Pt(),1)
                    hist_offhltpt_lead_r.Fill(tree.Offline_Matched_Taus[0].Pt(),1)
                if(i==1): 
                    hist_offhltpt_sublead.Fill(tree.Offline_Matched_Taus[1].Pt(),1)
                    hist_offhltpt_sublead_r.Fill(tree.Offline_Matched_Taus[1].Pt(),1)
            for j in range(len(tree.Off_Matched_TauRNN)):
                hist_offhltrnn.Fill(tree.Off_Matched_TauRNN[j],1)
            for k in range(len(tree.Off_Matched_TauProng)):
                hist_offhltprong.Fill(tree.Off_Matched_TauProng[k], 1)

    hltoff.append(hist_offhltpt)
    hltoff.append(hist_offhltpt_lead)
    hltoff.append(hist_offhltpt_sublead)
    hltoff.append(hist_offhltrnn)
    hltoff.append(hist_offhltprong)
    hltoff.append(hist_offhltpt_r)
    hltoff.append(hist_offhltpt_lead_r)
    hltoff.append(hist_offhltpt_sublead_r)
######################################################################################

####TrigMatched_Taus_HLTptfl##################################################################################
    hist_onhltptpt = ROOT.TH1D("onhltptpt","",200,0,1000)
    hist_onhltptpt_lead = ROOT.TH1D("onhltptpt_lead","",200,0,1000)
    hist_onhltptpt_sublead = ROOT.TH1D("onhltptpt_sublead","",200,0,1000)
    hist_onhltptrnn = ROOT.TH1D("onhltpt_rnn","",100,0,1)
    hist_onhltptprong = ROOT.TH1D("onhltpt_prong","",25,0,25)

    hist_onhltptpt_r = ROOT.TH1D("onhltptpt_r","",100,0,100)
    hist_onhltptpt_lead_r = ROOT.TH1D("onhltptpt_lead_r","",100,0,100)
    hist_onhltptpt_sublead_r = ROOT.TH1D("onhltptpt_sublead_r","",100,0,100)

    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT_1 = getattr(tree, "HLT_ETA25_r22")

        cond_pt = True
        cond_eta = True
        if cond_pt:
            for i in range(len(tree.TrigMatched_Taus_HLTptfl)):
                hist_onhltptpt.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                hist_onhltptpt_r.Fill(tree.TrigMatched_Taus_HLTptfl[i].Pt(),1)
                if(i==0): 
                    hist_onhltptpt_lead.Fill(tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                    hist_onhltptpt_lead_r.Fill(tree.TrigMatched_Taus_HLTptfl[0].Pt(),1)
                if(i==1): 
                    hist_onhltptpt_sublead.Fill(tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
                    hist_onhltptpt_sublead_r.Fill(tree.TrigMatched_Taus_HLTptfl[1].Pt(),1)
            for j in range(len(tree.TrigMatched_rnn_HLTptfl)):
                hist_onhltptrnn.Fill(tree.TrigMatched_rnn_HLTptfl[j],1)
            for k in range(len(tree.TrigMatched_prong_HLTptfl)):
                hist_onhltptprong.Fill(tree.TrigMatched_prong_HLTptfl[k], 1)
    
    hltpt.append(hist_onhltptpt)
    hltpt.append(hist_onhltptpt_lead)
    hltpt.append(hist_onhltptpt_sublead)
    hltpt.append(hist_onhltptrnn)
    hltpt.append(hist_onhltptprong)
    hltpt.append(hist_onhltptpt_r)
    hltpt.append(hist_onhltptpt_lead_r)
    hltpt.append(hist_onhltptpt_sublead_r)
######################################################################################

####TrigMatched_Taus_HLTetafl##################################################################################
    hist_onhltetapt = ROOT.TH1D("onhltetapt","",200,0,1000)
    hist_onhltetapt_lead = ROOT.TH1D("onhltetapt_lead","",200,0,1000)
    hist_onhltetapt_sublead = ROOT.TH1D("onhltetapt_sublead","",200,0,1000)
    hist_onhltetarnn = ROOT.TH1D("onhlteta_rnn","",100,0,1)
    hist_onhltetaprong = ROOT.TH1D("onhlteta_prong","",25,0,25)
    hist_onhltetapt_r = ROOT.TH1D("onhltetapt_r","",100,0,100)
    hist_onhltetapt_lead_r = ROOT.TH1D("onhltetapt_lead_r","",100,0,100)
    hist_onhltetapt_sublead_r = ROOT.TH1D("onhltetapt_sublead_r","",100,0,100)

    # Loop over entries
    for entry in entries:
        tree.GetEntry(entry)
        if taus[t] == "r22_Pass":
            HLT_1 = getattr(tree, "HLT_J25_r22")
            HLT_1 = getattr(tree, "HLT_ETA25_r22")

        cond_pt = True
        cond_eta = True
        if cond_eta:
            for i in range(len(tree.TrigMatched_Taus_HLTetafl)):
                hist_onhltetapt.Fill(tree.TrigMatched_Taus_HLTetafl[i].Pt(),1)
                hist_onhltetapt_r.Fill(tree.TrigMatched_Taus_HLTetafl[i].Pt(),1)
                if(i==0): 
                    hist_onhltetapt_lead.Fill(tree.TrigMatched_Taus_HLTetafl[0].Pt(),1)
                    hist_onhltetapt_lead_r.Fill(tree.TrigMatched_Taus_HLTetafl[0].Pt(),1)
                if(i==1): 
                    hist_onhltetapt_sublead.Fill(tree.TrigMatched_Taus_HLTetafl[1].Pt(),1)
                    hist_onhltetapt_sublead_r.Fill(tree.TrigMatched_Taus_HLTetafl[1].Pt(),1)
            for j in range(len(tree.TrigMatched_rnn_HLTetafl)):
                hist_onhltetarnn.Fill(tree.TrigMatched_rnn_HLTetafl[j],1)
            for k in range(len(tree.TrigMatched_prong_HLTetafl)):
                hist_onhltetaprong.Fill(tree.TrigMatched_prong_HLTetafl[k], 1)

    hlteta.append(hist_onhltetapt)
    hlteta.append(hist_onhltetapt_lead)
    hlteta.append(hist_onhltetapt_sublead)
    hlteta.append(hist_onhltetarnn)
    hlteta.append(hist_onhltetaprong)
    hlteta.append(hist_onhltetapt_r)
    hlteta.append(hist_onhltetapt_lead_r)
    hlteta.append(hist_onhltetapt_sublead_r)
######################################################################################
    for i in range(8):
        #posleg(leg_pos[i][0], leg_pos[i][1], leg_pos[i][2])
        hist_print_compare([hltoff[i],hltpt[i], hlteta[i]],
                ["off", "pt", "eta"],
                list_order[i], t)
        a = [ int(hltoff[i].GetEntries()), 
                int(hltpt[i].GetEntries()), 
                int(hlteta[i].GetEntries())]
        print("Efficiency pt/Off", a[1]/a[0])
        print("Efficiency eta/Off",a[2]/a[0])
        print("Efficiency eta/pt", a[2]/a[1])

##############Some Graph for Calculate Percentage Gain##############################################

    

def main():
    #tree_loop_deltaR("r22_Pass.root", 0)
    #tree_loop_hltpt("r22_Pass.root", 0)
    #hlteta = tree_loop_hlteta("r22_Pass.root", 0)
    #tree_loop_deltaR("r22_PassFail.root", 1)
    #tree_loop_hltpt("r22_PassFail.root", 1)
    #tree_loop_deltaR("Tau0_Pass.root", 2)
    #tree_loop_hltpt("Tau0_Pass.root", 2)
    tree_loop_deltaR("Tau0_PassFail.root", 3)
    tree_loop_hltpt("Tau0_PassFail.root", 3)


if __name__ == "__main__" :
    print("Hello, Start Ploting for HLT")
    main()


# Page4 
# inlcude tau0 trigger 
# emulate the trigger selection based on trigger object
# Highlight the dR and L1
# HLT (tau0 trigger ) JIRA number 

# h1: L1DR + ditau  (L1Topo)
# h2: di tau 4 jets

# Page 6 
# include L1Topo and di
# Just show one representative
# Show

# Page 7
# 1) Test trigger (Dev menu) JIRA Number/ 
# Plot From Javier
# Separate into two pages

# Page 8 
# find the tau12 
# Thanks menu experts for the prompt implementation
# Rate estimation from HLT reprocessing

# Page 8->9
# Highlight the right two points
# if we could have 80Hz, then the efficiency 
# First show the numbers then the plots.

# Page 9->10
# Rate @ 2e34 [Hz]
# withtout BDT 
# have the same performance

# Can we deploy 30 20 online
# deploy this to delayed or main
# Moved Already to physics menu

# Page 11 
# Remove the Additional information. 
# Rate estimation from HLT reporocesing/ Used the 
# Enhanced Biased sample for 
# Remove Run-3 for incoming data taking  

# Page 12 
# m_HH