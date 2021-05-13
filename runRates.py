import sys, os
import time
import ROOT as r
from ROOT import gSystem
from copy import deepcopy
import CMS_lumi
import myPlotter_input as effplot 
r.gROOT.SetBatch(True)
from subprocess import call
from markerColors import markerColors
from allLegends import legends as Legends


import argparse
parser = argparse.ArgumentParser(description='Plotter options')
parser.add_argument('-n','--ntuples', action='store_true', default = False)
parser.add_argument('-c','--compiler', action='store_true', default = False)
my_namespace = parser.parse_args()

################################# CHANGE BEFORE RUNNING #######################################

categories = ['norpc', 'rpc']
files = {'norpc':[], 'rpc':[], 'DM':[]}
#files['norpc'].append('nopu_noage_norpc')
#files['norpc'].append('mu_pu200_noage_norpc')
#files['norpc'].append('mu_PU200_withRPC_noAgeing_grouping2')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC')
files['norpc'].append('nu_PU250_noRPC_noAgeing_bkg9E34_debug')
files['norpc'].append('nu_PU250_noRPC_noAgeing_bkg9E34_20210223')
#files['norpc'].append('nu_pu250_noage_norpc')
#files['norpc'].append('nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000')
#files['rpc'].append('nu_pu250_noage_withrpc')
#files['rpc'].append('nu_pu250_age_withrpc_youngseg_muonage_norpcage_fail_3000')

#files['norpc'].append('PU200_nu_bkg7p5') 
#files['norpc'].append('PU250_nu_bkg9') 
#files['norpc'].append('PU200_nu_bkg7p5') 
#files['norpc'].append('nu_pu250_noage_norpc')
#files['norpc'].append('nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000')
#files['norpc'].append('PU0_bkgHits')
#files['norpc'].append('PU200_bkgHits')
#files['rpc'].append('pu200_age_withrpc_youngseg_muonage_norpcage_fail_3000')

r.gROOT.ForceStyle()
r.TGaxis.SetMaxDigits( 2 )
r.gROOT.ForceStyle()


totalQualities = [ "AllBX", "GoodBX", "GoodBX+index0", "GoodBX+index01","GoodBX+index012","GoodBX+index0123","AllBX+qu>=3","GoodBX+qu>=3", "GoodBX+matchedqu<3", "GoodBX+qu>=3+RPCseg", "GodBX+qu>=3+RPCseg+clus","GoodBX+matchedqu<3+RPCseg", "GoodBX+matchedqu<3+RPCseg+clus" ];

qualities_dict = {}
for i in range(len(totalQualities)) :
  qualities_dict [totalQualities[i]] = i+1

legends = ['AM'] #FIXME if more than 1 algo is used (as a lot more stuff)

qualities = {}
qualities['norpc'] = ["GoodBX","GoodBX+qu>=3"]
#qualities['norpc'] = ["GoodBX","GoodBX+qu>=3","GoodBX+index0", "GoodBX+index01","GoodBX+index012","GoodBX+index0123"]
qualities['rpc'] = ["GoodBX","GoodBX+qu>=3","GoodBX+matchedqu<3", "GoodBX+qu>=3+RPCseg", "GodBX+qu>=3+RPCseg+clus","GoodBX+matchedqu<3+RPCseg", "GoodBX+matchedqu<3+RPCseg+clus"]



plottingStuff = { 'lowlimityaxis' : 0,
		        'ranges' : {},
	          'markersize': 1,
	          'yaxistitleoffset': 1.5,
	          'xaxistitle': "Wheel",
	          'legxlow' : 0.3075 + 2 * 0.1975,
	          'legylow': 0.4,
	          'legxhigh': 0.9,
	          'legyhigh': 0.55,
	          'markertypedir':{},
	          'markercolordir':{}, 
	          'highLimitYAxis_perSector':{},  
              'PU':{}
   	          } 
#plottingStuff['ranges'] = {"rates":[60E6,10E6,10E6,10E6,10E6,10E6,50E6,10E6], "bandwidths":[60E8,10E8,10E8,10E8,10E8,10E8,50E8,10E8] }
plottingStuff['ranges']['nu_pu250_noage_norpc'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzer'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_PU250_noRPC_noAgeing_bkg9E34_debug'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_PU250_noRPC_noAgeing_bkg9E34_20210223'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_pu250_noage_withrpc'] = { "rates":[15E5,15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['nu_pu250_age_withrpc_youngseg_muonage_norpcage_fail_3000'] = { "rates":[15E5,15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['PU0_bkgHits'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1.5E8,1.5E8,1.5E8,1.5E8,1.5E8,1.5E8] }
plottingStuff['ranges']['PU200_bkgHits'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1.5E8,1.5E8,1.5E8,1.5E8,1.5E8,1.5E8] }
plottingStuff['ranges']['PU200_nu_bkg7p5'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1.5E8,1.5E8,1.5E8,1.5E8,1.5E8,1.5E8] }
plottingStuff['ranges']['PU250_nu_bkg9'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1.5E8,1.5E8,1.5E8,1.5E8,1.5E8,1.5E8] }
plottingStuff['ranges']['nopu_noage_norpc'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['pu200_noage_norpc'] = {"rates":[15E5,15E5,15E5,15E5,15E5,15E5], "bandwidths":[1E8,1E8,1E8,1E8,1E8,1E8] }
plottingStuff['ranges']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC'] = {"rates":[1E7,1E7,1E7,1E7,1E7,1E7], "bandwidths":[1E9,1E9,1E9,1E9,1E9,1E9] }
plottingStuff['ranges']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel'] = {"rates":[1E7,1E7,1E7,1E7,1E7,1E7], "bandwidths":[1E9,1E9,1E9,1E9,1E9,1E9] }


plottingStuff['highLimitYAxis_perSector']['default'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_pu250_noage_norpc'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzer'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_PU250_noRPC_noAgeing_bkg9E34_debug'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_PU250_noRPC_noAgeing_bkg9E34_20210223'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_pu250_noage_withrpc'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nu_pu250_age_withrpc_youngseg_muonage_norpcage_fail_3000'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['PU0_bkgHits'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['PU200_bkgHits'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['PU200_nu_bkg7p5'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['PU250_nu_bkg9'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['nopu_noage_norpc'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['pu200_noage_norpc'] = 200E6;  
plottingStuff['highLimitYAxis_perSector']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC'] = 300E7;  
plottingStuff['highLimitYAxis_perSector']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel'] = 300E7;  




plottingStuffRat = { 'lowlimityaxis' : {},
	             'markersize': 1,
	             'yaxistitleoffset': 1.5,
	             'xaxistitle': "Wheel",
	             'legxlow' : 0.3075 + 2 * 0.1975,
	             'legylow': 0.4,
	             'legxhigh': 0.9,
	             'legyhigh': 0.5,
	             'markertypedir':{},
	             'markercolordir':{},  
               'PU':{}
   	           }   
plottingStuffRat['lowlimityaxis']['default'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['nu_pu250_noage_norpc'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzer'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['nu_PU250_noRPC_noAgeing_bkg9E34_debug'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['nu_PU250_noRPC_noAgeing_bkg9E34_20210223'] = [0,0,0,0,0]
#plottingStuffRat['lowlimityaxis']['nu_pu250_noage_norpc'] = [0.4,0.4,0.4,0.4,0.4]
plottingStuffRat['lowlimityaxis']['nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000'] = [0,0,0,0,0]
#plottingStuffRat['lowlimityaxis']['nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000'] = [0.4,0.4,0.4,0.4,0.4]
plottingStuffRat['lowlimityaxis']['nu_pu250_noage_withrpc'] = [0,0,0,0,0,0,0]
#plottingStuffRat['lowlimityaxis']['nu_pu250_noage_withrpc'] = [0.5,0.5,0.5,0.5]
plottingStuffRat['lowlimityaxis']['nu_pu250_age_withrpc_youngseg_muonage_norpcage_fail_3000'] = [0,0,0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['PU0_bkgHits'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['PU200_bkgHits'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['PU200_nu_bkg7p5'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['PU250_nu_bkg9'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['nopu_noage_norpc'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['pu200_noage_norpc'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC'] = [0,0,0,0,0]
plottingStuffRat['lowlimityaxis']['DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel'] = [0,0,0,0,0]

#legends = {'norpc':[],'rpc':[], 'DM':[]}
#legends['norpc'] = ['All','Quality>2','index0','index01','index012','index0123']
#legends['rpc'] = ['All','Without Quality<3', 'With RPC-matched Quality<3' ,'Quality>2 + RPC hits','With RPC-matched Quality<3 + RPC hits']
#legends['DM'] = ['']


##############################################################################################

if my_namespace.ntuples == True :
    print ("Starting ntuplizer for every sample in input")
    time.sleep(2)
    r.gInterpreter.ProcessLine(".x loadTPGSimAnalysis_Rates.C")
    gSystem.Load(os.getcwd() + "/DTNtupleBaseAnalyzer_C.so")
    gSystem.Load(os.getcwd() + "DTNtupleTPGSimAnalyzer_Rates_C.so")
    from ROOT import DTNtupleTPGSimAnalyzer
else : 
  print("Not making ntuples. If you want to make them, restart with 'yes' as first argument ")
  time.sleep(2)

path = '/eos/home-j/jleonhol/simulationSamples/'
ratePath = "./plotsRates/"
#outputPath = './ntuples/'
outputPath = '/eos/home-j/jleonhol/ntuplesResults/'
plotscaffold = { "rates": "ratePrims_{al}_{wh}_{se}_{st}", "bandwidths": "bandwidth_{al}_{wh}_{se}_{st}" }
savescaffold = { "rates": "hRates", "bandwidths": "hBandwidths" }
savescaffoldTot = { "rates": "hRatesTot", "bandwidths": "hBandwidthsTot" }
#markerColors = [r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta]

if not os.path.isdir(ratePath) : rc = call('mkdir ' + ratePath, shell=True)

for cat in files : 
  for fil in files[cat] :
    rc = call('mkdir ' + ratePath + fil, shell=True) 
    if my_namespace.ntuples == True :
      print ('Obtaining rate ntuples for ' + fil)
      time.sleep(2) 
      analysis = DTNtupleTPGSimAnalyzer(path + fil + '.root', outputPath + 'results_rates_' + fil + '.root')
      analysis.Loop()

    print "\nBeginning plotting\n"


    for plot in ['bandwidths']: 
      for i in range (len(qualities[cat])) : 
        listofplots = []     
        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil] = 20
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil] = markerColors[0]
        effplot.makeRatesPerRingplot(listofplots, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
        effplot.combineRatesPerRingplots(listofplots, i, legends, plot, plottingStuff, ratePath + fil, fil,  savescaffold[plot] )

        effplot.makeRatesPerSectorplot("AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot], plottingStuff, savescaffold[plot], plot, ratePath + fil, i)
        

    for plot in ['rates']: 
      listofplots = []     
      plottingStuff['markertypedir']["h_" + "AM" + "_" + fil] = 20
      plottingStuff['markercolordir']["h_" + "AM" + "_" + fil] = markerColors[0]
      effplot.makeRatesPerRingplot(listofplots, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][0]], plotscaffold[plot])
      effplot.combineRatesPerRingplots(listofplots, 0, legends, plot, plottingStuff, ratePath + fil, fil,  savescaffold[plot] )

      for i in range (1,len(qualities[cat])) : 
        listofplots2 = []     
        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil] = 20
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil] = markerColors[0]
        effplot.makeRatesPerRingplot(listofplots2, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
        effplot.combineRatesPerRingplots(listofplots2, i, legends, plot, plottingStuff, ratePath + fil, fil,  savescaffold[plot] )
        effplot.combineRateRatiosPerRingplots(listofplots2, listofplots, ratePath + fil, fil, i, plottingStuffRat,legends)
      
for cat in files : 
  rc = call('mkdir ' + ratePath + cat, shell=True)
  if len(files[cat]) == 0 : continue 
  for plot in ['bandwidths']: 
    for i in range (len(qualities[cat])) : 
      listofplots = []     
      num=0
      myLegends = []
      for fil in files[cat] :
        myLegends.append(Legends[fil])
        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil] = 20
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil] = markerColors[num]
        num+=1
        effplot.makeRatesPerRingplot(listofplots, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
        #effplot.makeRatesPerRingplot(listofplots, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
      effplot.combineRatesPerRingplots(listofplots, i, myLegends, plot, plottingStuff, ratePath + cat, fil,  savescaffold[plot] )
      #effplot.combineRatesPerRingplots(listofplots, i, ['No aging','Aging 3000fb^{-1}'], plot, plottingStuff, ratePath + cat, fil,  savescaffold[plot] )

        

  for plot in ['rates']: 
    listofplots2 = {}     
    listofplots3 = []    
    myLegends2 = []    
    for i in range (len(qualities[cat])) : 
      listofplots2[i] = []     
      num=0
      myLegends = []
      for fil in files[cat] :
        myLegends.append(Legends[fil])
        myLegends2.append(Legends[fil+qualities[cat][i]])
        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil] = 20
        plottingStuff['markercolordir'][num] = markerColors[num]
        num+=1
        effplot.makeRatesPerRingplot(listofplots2[i], "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
        effplot.makeRatesPerRingplot(listofplots3, "AM", fil, outputPath + 'results_rates_' + fil + '.root', qualities_dict[qualities[cat][i]], plotscaffold[plot])
      if len(files[cat]) == 2 : effplot.divideRatesPerRingplots(listofplots2[i][0], listofplots2[i][1], ratePath + cat, fil, i, plottingStuffRat, myLegends)
      effplot.combineRatesPerRingplots(listofplots2[i], i, myLegends, plot, plottingStuff, ratePath + cat, fil,  savescaffold[plot] )
      #effplot.combineRatesPerRingplots(listofplots2[i], i, ['No aging','Aging 3000fb^{-1}'], plot, plottingStuff, ratePath + cat, fil,  savescaffold[plot] )
      effplot.combineRateRatiosPerRingplots(listofplots2[i], listofplots2[0], ratePath + cat, fil, i, plottingStuffRat, myLegends)
      #effplot.combineRateRatiosPerRingplots(listofplots2[i], listofplots2[0], ratePath + cat, fil, i, plottingStuffRat, ['No aging','Aging 3000fb^{-1}'])
    
    effplot.combineRatesPerRingplots(listofplots3, 0, myLegends2, plot, plottingStuff, ratePath + cat, fil,  savescaffoldTot[plot] )
      #effplot.combineRatesPerRingplots(listofplots2[i], i, ['No aging','Aging 3000fb^{-1}'], plot, plottingStuff, ratePath + cat, fil,  savescaffold[plot] )



