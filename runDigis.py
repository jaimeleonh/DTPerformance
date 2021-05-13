import sys, os
import time
import ROOT as r
from ROOT import gSystem
from copy import deepcopy
import CMS_lumi
r.gROOT.SetBatch(True)
from subprocess import call
import myPlotter_input as effplot
from markerColors import markerColors

import argparse
parser = argparse.ArgumentParser(description='Plotter options')
parser.add_argument('-n','--ntuples', action='store_true', default = False)
my_namespace = parser.parse_args()

################################# CHANGE BEFORE RUNNING #######################################

categories = ['norpc', 'rpc']
files = {'norpc':[], 'rpc':[], 'DM':[]}
#files['norpc'].append('PU200_mu_bkg7p5') 
#files['norpc'].append('pu200_noage_norpc') 
#files['norpc'].append('nopu_noage_norpc') 
files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel')
#files['norpc'].append('PU250_nu_bkg9') 
#files['norpc'].append('PU200_bkgHits') 

##############################################################################################

if my_namespace.ntuples == True : 
    print ("Starting ntuplizer for every sample in input")
    time.sleep(2)
    r.gInterpreter.ProcessLine(".x loadTPGSimAnalysis_Digis.C")
    gSystem.Load(os.getcwd() + "/DTNtupleBaseAnalyzer_C.so")
    gSystem.Load(os.getcwd() + "/DTNtupleTPGSimAnalyzer_Digis_C.so")
    from ROOT import DTNtupleTPGSimAnalyzer
else : 
  print("Not making ntuples. If you want to make them, restart with 'yes' as first argument ")
  time.sleep(2)

path = '/eos/home-j/jleonhol/simulationSamples/'
plotsPath = "./digiPlots/"
#outputPath = './ntuples/'
outputPath = '/eos/home-j/jleonhol/ntuplesResults/'
eosPath='/eos/home-j/jleonhol/www/resolutionsNote/'

if not os.path.isdir(plotsPath) : rc = call('mkdir ' + plotsPath, shell=True)

chambTag = ["MB1", "MB2", "MB3", "MB4"]
wheelTag    = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
magnitude = ["Time", "Phi", "PhiB", "TanPsi", "x"]

plottingStuff = { 'lowlimityaxis': 0,
		      'highlimityaxis': {},
		      'markersize': 1,
              'yaxistitle' : {"Time":"Time resolution (ns)", "Phi":"Global Phi resolution (mrad)", "PhiB":"Bending Phi resolution (mrad)", "TanPsi":"Local direction resolution (mrad)", "x":"Position resolution (cm)"}, 
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': "Wheel",
		      'legxlow' : 0.85,
		      'legylow': 0.85,
		      'legxhigh': 0.99,
		      'legyhigh': 0.99,
		      'markertypedir':{},
		      'markercolordir':{}  
   		    }

plottingStuff['highlimityaxis']['Time'] = {'3h': 5, '4h': 5}
plottingStuff['highlimityaxis']['Phi'] = {'3h': 50E-3, '4h':50E-3}
plottingStuff['highlimityaxis']['PhiB'] = {'3h': 15,  '4h': 10}
plottingStuff['highlimityaxis']['TanPsi'] = {'3h': 15, '4h': 10}
plottingStuff['highlimityaxis']['x'] = {'3h': 0.02, '4h': 0.02}

#markerColors = [r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta]


for cat in files :  
  for fil in files[cat] :
    if my_namespace.ntuples == True :     
      print ('Obtaining resolution ntuples for ' + fil )
      time.sleep(2) 
      analysis = DTNtupleTPGSimAnalyzer(path + fil + '.root', outputPath + 'results_digis_' +fil + '_.root')
      analysis.Loop()
     
    c   = r.TCanvas("c", "c", 1200, 800)
    res = r.TFile.Open(  outputPath + 'results_digis_' +fil + '_.root' )
    plot = res.Get("DigiDistr")
    plot.Draw()
    c.SaveAs(plotsPath + "DigiDistr_"+ fil + ".png")
    c.SaveAs(plotsPath + "DigiDistr_"+ fil + ".pdf")
    c.SaveAs(plotsPath + "DigiDistr_"+ fil + ".root")

    for i in range(1,5):
        c1   = r.TCanvas("c", "c", 1200, 800)
        plot = res.Get("hits_MB" + str(i))
        plot.Draw("colztext")
        c1.SaveAs(plotsPath + "digi_rate_{}_MB{}.png".format(fil, i))
        c1.SaveAs(plotsPath + "digi_rate_{}_MB{}.pdf".format(fil, i))
        c1.SaveAs(plotsPath + "digi_rate_{}_MB{}.root".format(fil, i))

