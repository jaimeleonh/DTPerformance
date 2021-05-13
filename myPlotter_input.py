# -*- coding: utf-8 -*-
import ROOT as r
from copy import deepcopy
import CMS_lumi
import sys
from lookForPU import lookForPU 
from markerColors import markerColors
r.gROOT.SetBatch(True)



############################################# CHANGE IF NECESSARY ###########################################################


def main() :

  path = "./plotsEff/"
  outputPath = './ntuples/'

  File = sys.argv[1]
  qualities = ['','nothreehits','index0','index01','index012','index0123']

  prefixes = "results_"
  suffixes = ".root"
  legends = ['All','Quality>2','index0','index01','index012','index0123']

  plottingStuff = { 'lowlimityaxis': 0.9,
		    'highlimityaxis': 1,
		    'markersize': 1,
		    'yaxistitle' : 'Efficiency (adim.)',
		    'yaxistitleoffset': 1.5,
		    'xaxistitle': "Wheel",
		    'legxlow' : 0.3075 + 2 * 0.1975,
		    'legylow': 0.3,
		    'legxhigh': 0.9,
		    'legyhigh': 0.5,
		    'markerColors':[r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta],
		    'markertypedir':{},
		    'markercolordir':{},
	  	  }   


  markerColors = [r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta]
  print "\nBeginning plotting\n"

  plotscaffold = "hEff_{st}_{al}_{ty}"
  savescaffold = "hEff_" + File 

  listofplots = []     
  
  for i in range (len(qualities)) : 
    plottingStuff['markertypedir']["hEff_" + "AM" + "_" + qualities[i]] = 20
    plottingStuff['markercolordir']["hEff_" + "AM" + "_" + qualities[i]] = markerColors[i]
    makeresplot(listofplots, "AM", qualities[i], outputPath + prefixes + File + '_' + qualities[i] + suffixes, plotscaffold)


  print "\nCombining and saving\n"
  combineresplots(listofplots, legends, plottingStuff, path,  savescaffold )


#############################################################################################################################


def makeResolPlot(hlist, algo, suffix, fileName, plotscaffold):
    print "Obtaining intermediate plot for algo ", algo
    wheelTag = ["Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    res = r.TFile.Open(fileName)

    hmatched = [res.Get(plotscaffold.format(al = algo, wh = wheelTag[iwh])) for iwh in range(5)]
    resplot = r.TH1F("h_{al}_{su}".format(al = algo, su = suffix), "", 20, -0.5, 19.5)


    ibin = 1
    for ich in range(1,5):
    	for iwh in range(5):
            resplot.SetBinContent(ibin, hmatched[iwh].GetBinContent(ich))
            ibin += 1

    hlist.append(deepcopy(resplot))
    res.Close(); del hmatched, res, resplot
    return

def makeresplot(hlist, algo, suffix, fileName, plotscaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    print "Obtaining intermediate plot for algo ", algo
    res = r.TFile.Open(fileName)
    hmatched = [res.Get(plotscaffold.format(al = algo, st = chambTag[ich], ty = "matched")) for ich in range(4)]
    htotal   = [res.Get(plotscaffold.format(al = algo, st = chambTag[ich], ty = "total")) for ich in range(4)]

    resplot = r.TH1F("hEff_{al}_{su}".format(al = algo, su = suffix), "", 20, -0.5, 19.5)
    
    ibin = 1
    for ich in range(4):
        for iwh in range(1, 6):
          #  print ich+1, iwh-3, ibin
            resplot.SetBinContent(ibin, hmatched[ich].GetBinContent(iwh) / htotal[ich].GetBinContent(iwh))
            eff = r.TEfficiency('kk','',1,-0.5,0.5)
            eff.SetTotalEvents(1, int(htotal[ich].GetBinContent(iwh)))
            eff.SetPassedEvents(1,int(hmatched[ich].GetBinContent(iwh)))
            if (eff.GetEfficiencyErrorLow(1)-eff.GetEfficiencyErrorUp(1)) > 0.05: print 'warning, bin asymmetric'
            resplot.SetBinError( ibin, max(eff.GetEfficiencyErrorLow(1),eff.GetEfficiencyErrorUp(1)))
            del eff
            ibin += 1

    hlist.append(deepcopy(resplot))
    res.Close(); del hmatched, htotal, res, resplot
    return

def makeWhateverResplot(hlist, algo, suffix, fileName, plotscaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    print "Obtaining intermediate plot for algo ", algo
    res = r.TFile.Open(fileName)
    hmatched = res.Get(plotscaffold.format(al = algo, ty = "matched")) 
    htotal   = res.Get(plotscaffold.format(al = algo, ty = "total")) 
    hmatched.Rebin(2)
    htotal.Rebin(2)

    eff = r.TGraphAsymmErrors(hmatched, htotal)
    #eff = r.TEfficiency(hmatched, htotal)
    eff.SetName("hEff_{al}_{su}".format(al = algo, su = suffix))

    hlist.append(deepcopy(eff))

    res.Close(); del hmatched, htotal, eff
    return


def makeRatesPerRingplot(hlist, algo, suffix, fileName,binToUse,plotScaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    sectorTag = ["Sec1","Sec2","Sec3","Sec4","Sec5","Sec6","Sec7","Sec8","Sec9","Sec10","Sec11","Sec12"]
    print "Obtaining intermediate plot for algo ", algo
    res = r.TFile.Open(fileName)
    #hmatched = [res.Get(plotscaffold.format(mag = magnit + "Res", qu = quality, al = algo, wh = wheelTag[iwh])) for iwh in range(5)]
    hmatched = []
    for ich in range(4):
      for iwh in range(5):
        for ise in range(12):
          hmatched.append(res.Get(plotScaffold.format(al = algo, wh = wheelTag[iwh], se=sectorTag[ise], st=chambTag[ich]) ))
    resplot = r.TH1F("h_{al}_{su}".format(su = suffix, al = algo), "", 20, -0.5, 19.5)
    
    ibin = 1
    resplot.GetYaxis().SetTitle(hmatched[0].GetXaxis().GetBinLabel(binToUse))
    for ich in range(4) :
      for iwh in range(5):
        content = 0
        for ise in range(12):
          content += hmatched[(5*12)*ich + 12*iwh + ise].GetBinContent(binToUse)
        resplot.SetBinContent(ibin, content / 12.0)
        ibin += 1
    hlist.append(deepcopy(resplot))
    res.Close(); del hmatched, res, resplot
    return

def makeRatesPerSectorplot(algo, suffix, fileName,binToUse,plotScaffold, plottingStuff, savescaffold, whatToPlot, path, index):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    sectorTag = ["Sec1","Sec2","Sec3","Sec4","Sec5","Sec6","Sec7","Sec8","Sec9","Sec10","Sec11","Sec12"]
    print "Obtaining intermediate plot for algo ", algo
    res = r.TFile.Open(fileName)
    hmatched = []
    for ise in range(12):
      for iwh in range(5):
        for ich in range(4):
          hmatched.append(res.Get(plotScaffold.format(al = algo, wh = wheelTag[iwh], se=sectorTag[ise], st=chambTag[ich]) ))
    
    c   = r.TCanvas("c", "c", 1200, 800)
    c.SetGrid()
    leg = r.TLegend(0.7,0.7,0.9,0.9)

    markerColors = [r.kBlue, r.kRed, r.kMagenta, r.kBlack, r.kGreen]
    resplots = []
    for iwh in range(5):
      resplots.append( r.TH1F("h_{al}_{su}".format(su = suffix + wheelTag[iwh], al = algo), "", 12, -0.5, 11.5) )
      resplot = resplots[iwh]
      resplot.GetYaxis().SetTitle("Bandwidth (bps) - " + hmatched[0].GetXaxis().GetBinLabel(binToUse))
      ibin = 1
      for ise in range(12):
        content = 0;
        for ich in range(4):
          content += hmatched[(5*4)*ich + 4*iwh + ich].GetBinContent(binToUse)
        resplot.SetBinContent(ibin, content)
        ibin += 1
    	     
      resplot.SetStats(False)
      resplot.GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highLimitYAxis_perSector'][suffix])
      resplot.GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
      resplot.GetXaxis().SetTitle("Sector")
      resplot.GetXaxis().SetNdivisions(12)
      resplot.SetMarkerSize(plottingStuff['markersize'])
      resplot.SetMarkerStyle(20)
      resplot.SetMarkerColor(markerColors[iwh])
      for ilabel in range(1, 13):
        resplot.GetXaxis().SetBinLabel(ilabel, str(ilabel))
      resplot.Draw("P,hist" + (ilabel!=1)*'same')
        
      leg.AddEntry(resplots[iwh], wheelTag[iwh], "P")
    
  #	CMS_lumi.lumi_13TeV = ""
   # 	CMS_lumi.extraText  = 'Simulation - No ageing'
  # 	CMS_lumi.cmsTextSize= 0.5
  # 	CMS_lumi.lumi_sqrtS = ''
  #  	CMS_lumi.CMS_lumi(r.gPad, 0, 0, 0.07)
      firsttex = r.TLatex()
      firsttex.SetTextSize(0.03)
      firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
      firsttex.Draw("same");

      secondtext = r.TLatex()
      toDisplay = r.TString()
      if (lookForPU(suffix) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(suffix)) + " PU")
      else :  toDisplay  = r.TString("14 TeV")
      secondtext.SetTextSize(0.035)
      secondtext.SetTextAlign(31)
      secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
      secondtext.Draw("same")


    #c.SetLogy()
    leg.Draw()
    c.SaveAs(path + '/' + savescaffold + '_' + str(index+1) + '_perWheel.png')
    c.SaveAs(path + '/' + savescaffold + '_' + str(index+1) + '_perWheel.pdf')
    c.SaveAs(path + '/' + savescaffold + '_' + str(index+1) + '_perWheel.root')
    c.Close(); del c

    res.Close(); del hmatched, res, resplots
    return


def combineEffPlots(hlist, legends, plottingStuff, path, savescaffold): 
    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)
    #hlist[0].GetPaintedGraph().GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'])
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    hlist[0].GetYaxis().SetTitle(plottingStuff['yaxistitle'])
    #hlist[0].GetPaintedGraph().GetXaxis().SetTitle(plottingStuff['xaxistitle'])

    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        hlist[iplot].SetLineColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        #hlist[iplot].SetMarkerSize(plottingStuff['markersize'])
        hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        #hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        leg.AddEntry(hlist[iplot], legends[iplot], "PL")
        hlist[iplot].Draw("P" + (iplot == 0) * "A"+(iplot != 0) * "same")

    leg.Draw()
   
    r.gPad.Update()
    #hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'])
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'])
    #graph = hlist[0].GetPaintedGraph()
    #graph.SetMinimum(plottingStuff['lowlimityaxis'])
    #graph.SetMaximum(plottingStuff['highlimityaxis'])
    hlist[0].SetTitle("; " + plottingStuff['xaxistitle'] + "; " + plottingStuff['yaxistitle'])
    #hlist[0].GetPaintedGraph().SetTitle("; " + plottingStuff['xaxistitle'] + "; Efficiency")
    
    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if ( 'PU' in plottingStuff ) :
      if ('writeInPlot' in plottingStuff) :
        toDisplay  = r.TString(plottingStuff['writeInPlot'] + ", 14 TeV, " + str(plottingStuff['PU'])  +" PU")
      else :
        toDisplay  = r.TString("14 TeV, " + str(plottingStuff['PU'])  +" PU")
    else : 
      if ('writeInPlot' in plottingStuff) :
        toDisplay  = r.TString(plottingStuff['writeInPlot'] + ", 14 TeV")
      else :
        toDisplay  = r.TString("14 TeV")
    
    
    
    
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")

    #if ('writeInPlot' in plottingStuff): 
    #  print "True"
    #  textlist = []
    #  textlist.append(r.TText( 0.8 , 0.85, plottingStuff['writeInPlot']))
    #  textlist[-1].SetNDC(True)
    #  textlist[-1].Draw("same")

    #c.SetLogy()
    c.SaveAs(path + savescaffold + ".png")
    c.SaveAs(path + savescaffold + ".pdf")
    c.SaveAs(path + savescaffold + ".root")
    c.Close(); del c
    return


def combineresplots(hlist, legends, plottingStuff, path, savescaffold, fil):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()
    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'])
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    hlist[0].GetYaxis().SetTitle(plottingStuff['yaxistitle'])
    hlist[0].GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist[0].GetXaxis().SetNdivisions(120)

    ilabel = 1
    for ich in range(4):
        for iwh in range(-2, 3):
            hlist[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1

   
    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerSize(plottingStuff['markersize'])
        # hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        # hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][iplot])
        hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][iplot])
        leg.AddEntry(hlist[iplot], legends[iplot], "P")
        hlist[iplot].Draw("P,hist" + (iplot != 0) * "same")

    leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.20, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    if (plottingStuff['highlimityaxis'] > 1.01) : firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    else : firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if (lookForPU(fil) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(fil))  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")

    #c.SetLogy()
    c.SaveAs(path + savescaffold + ".png")
    c.SaveAs(path + savescaffold + ".pdf")
    c.SaveAs(path + savescaffold + ".root")
    c.Close(); del c
    return

def combineRatesPerRingplots(hlist, binToUse, legends, whatToPlot, plottingStuff, path, fil, savescaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    sectorTag = ["Sec1","Sec2","Sec3","Sec4","Sec5","Sec6","Sec7","Sec8","Sec9","Sec10","Sec11","Sec12"]
    units = {'bandwidths': 'Bandwidth (bps)', 'rates': 'Rate (Hz)'}


    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()
    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['ranges'][fil][whatToPlot][binToUse])
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    hlist[0].GetYaxis().SetTitle('Mean per sector ' +  units[whatToPlot] + ' - '  + hlist[0].GetYaxis().GetTitle() )
    #hlist[0].GetYaxis().TGaxis.SetMaxDigits(2)
    hlist[0].GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist[0].GetXaxis().SetNdivisions(120)
    #print ('shit ' + hlist[0].GetYaxis().GetMaxDigits())

    ilabel = 1
    for ich in range(4):
      for iwh in range(-2, 3):
        hlist[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
        ilabel += 1

    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerSize(plottingStuff['markersize'])
        hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        hlist[iplot].SetMarkerColor( markerColors[iplot])
        #hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        leg.AddEntry(hlist[iplot], legends[iplot], "P")
        hlist[iplot].Draw("P,hist" + (iplot != 0) * "same")

    leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.80, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    #cmslat = r.TLatex()
    #cmslat.SetTextSize(0.03);
    #cmslat.DrawLatexNDC(0.11, 0.91, "#scale[1.5]{CMS}");
    #cmslat.Draw("same");

    #CMS_lumi.lumi_13TeV = ""
    #CMS_lumi.extraText  = 'Simulation'
    #CMS_lumi.cmsTextSize= 0.5
    #CMS_lumi.lumi_sqrtS = ''

    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if (lookForPU(fil) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(fil))  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")

    #r.TGaxis.SetMaxDigits(2)
    #print (r.TGaxis.GetMaxDigits())
    #r.gPad.Modified() 
    #r.gPad.Update() 
   # c.Update()
    
    r.TGaxis.SetMaxDigits(4)
    r.gPad.Update()
    c.Update()
    #c.SetLogy()
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".png")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".pdf")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".root")
    c.Close(); del c
    return

def combineRatesPerSectorplots(hlist, binToUse, legends, whatToPlot, plottingStuff, path, fil, savescaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    sectorTag = ["Sec1","Sec2","Sec3","Sec4","Sec5","Sec6","Sec7","Sec8","Sec9","Sec10","Sec11","Sec12"]
    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()
    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['ranges'][fil][whatToPlot][binToUse])
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    hlist[0].GetYaxis().SetMaxDigits(9)
    #hlist[0].GetYaxis().SetTitle(magnitude[index] + " resolution " + units[index])
    hlist[0].GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist[0].GetXaxis().SetNdivisions(120)
    ilabel = 1
    for ich in range(4):
        for iwh in range(-2, 3):
            hlist[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1

    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerSize(plottingStuff['markersize'])
        hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        leg.AddEntry(hlist[iplot], legends[iplot], "P")
        hlist[iplot].Draw("P,hist" + (iplot != 0) * "same")

    #leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.80, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    #cmslat = r.TLatex()
    #cmslat.SetTextSize(0.03);
    #cmslat.DrawLatexNDC(0.11, 0.91, "#scale[1.5]{CMS}");
    #cmslat.Draw("same");

    #CMS_lumi.lumi_13TeV = ""
    #CMS_lumi.extraText  = 'Simulation'
    #CMS_lumi.cmsTextSize= 0.5
    #CMS_lumi.lumi_sqrtS = ''

    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if (lookForPU(fil) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(fil))  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")

    r.TGaxis.SetMaxDigits(4)
    r.gPad.Update()
    c.Update()

    #c.SetLogy()
    c.SaveAs(path + "/" + fil+ "/" + savescaffold + str(binToUse+1) + ".png")
    c.SaveAs(path + "/" + fil+ "/" + savescaffold + str(binToUse+1) + ".pdf")
    c.SaveAs(path + "/" + fil+ "/" + savescaffold + str(binToUse+1) + ".root")
    c.Close(); del c
    return

def combineRateRatiosPerRingplots(hlist, hlist2, path, fil, binToUse, plottingStuff, legends):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    
    leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    #hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'][fil][binToUse-1], 1E7)
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'][fil][binToUse-1], 1)
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    #hlist[0].GetYaxis().SetMaxDigits(2)
    hlist[0].GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist[0].GetXaxis().SetNdivisions(120)
    
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()

    hratio = []
    for iplot in range(len(hlist)):
        hratio.append(hlist[iplot].Clone())
        hratio[iplot].Divide(hlist2[iplot])
        leg.AddEntry(hratio[iplot], legends[iplot], "p")
        #leg.AddEntry(hlist[iplot], legends[iplot], "p")
        #hlist[iplot].Draw("p,hist,same")
        hratio[iplot].SetMarkerSize(plottingStuff['markersize'])
        hratio[iplot].SetMarkerStyle(20)
        hratio[iplot].SetMarkerColor(r.kBlue)
        hratio[iplot].Draw("p,hist" + (iplot != 0) * "same")
        #hlist2[iplot].Draw("p,hist" + (iplot != 0) * "same")

    ilabel = 1
    
    for ich in range(4):
        for iwh in range(-2, 3):
            hratio[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1
    leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.30, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if (lookForPU(fil) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(fil))  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")
    
    r.TGaxis.SetMaxDigits(4)
    r.gPad.Update()
    c.Update()

    savescaffold = 'hRatios' 
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".png")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".pdf")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".root")
    c.Close(); del c
    return



def combineResolPlots(hlist, mag, quality, legends, plottingStuff, path, savescaffold):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    print "Combining list of plots"
    if len(hlist) == 0: raise RuntimeError("Empty list of plots")
    
    hlist[0].SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'], plottingStuff['highlimityaxis'][mag][quality])
    hlist[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    #hlist[0].GetYaxis().SetMaxDigits(2)
    hlist[0].GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist[0].GetYaxis().SetTitle(plottingStuff['yaxistitle'][mag])
    hlist[0].GetXaxis().SetNdivisions(120)
    
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()
    
    if legends : leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
  
    ilabel=1
    for ich in range(4):
        for iwh in range(-2, 3):
            hlist[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1

    for iplot in range(len(hlist)):
        hlist[iplot].SetMarkerSize(plottingStuff['markersize'])
        hlist[iplot].SetMarkerStyle(plottingStuff['markertypedir'][hlist[iplot].GetName()])
        hlist[iplot].SetMarkerColor(plottingStuff['markercolordir'][hlist[iplot].GetName()])
        if legends: leg.AddEntry(hlist[iplot], legends[iplot], "P")
        hlist[iplot].Draw("P,hist" + (iplot != 0) * "same")

    if legends: leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.80, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")


    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if ("PU" in plottingStuff) : toDisplay  = r.TString("14 TeV, " + str(plottingStuff["PU"])  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    
    toDisplay = r.TString("14 TeV, 3000 fb^{-1}, 200 PU") #typically for Phase-2
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")
    
    r.TGaxis.SetMaxDigits(3)
    r.gPad.Update()
    c.Update()

    c.SaveAs(path + "/" + savescaffold + ".png")
    c.SaveAs(path + "/" + savescaffold + ".pdf")
    c.SaveAs(path + "/" + savescaffold + ".root")
    c.Close(); del c
    return




def divideRatesPerRingplots(hlist, hlist2, path, fil, binToUse, plottingStuff, legends):
    chambTag = ["MB1", "MB2", "MB3", "MB4"]
    wheelTag = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
    
    #leg = r.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
    hlist.SetStats(False)
    #hlist[0].SetTitle("L1 DT Phase 2 algorithm efficiency comparison")
    #hlist[0].GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'][fil][binToUse-1], 1E7)
    hlist.GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'][fil][binToUse-1], 3.5)
    #hlist.GetYaxis().SetRangeUser(plottingStuff['lowlimityaxis'][fil][binToUse-1], 1)
    hlist.GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
    #hlis[0].GetYaxis().SetMaxDigits(2)
    hlist.GetXaxis().SetTitle(plottingStuff['xaxistitle'])
    hlist.GetXaxis().SetNdivisions(120)
    
    c   = r.TCanvas("c", "c", 800, 800)
    c.SetLeftMargin(0.11)
    c.SetGrid()

    hratio = []
   # for iplot in rage(len(hlisVt)):
    for iplot in range(1) :
     #   for ich in range(4):
     #       for iwh in range(-2, 3):
     #           print (str(hlist.GetBinContent( iwh + 2 + 1 + 5 * ich )) + " , " + str(hlist2.GetBinContent( iwh + 2 + 1 + 5 * ich )) )
        
        
        hratio.append(hlist.Clone())
        hratio[iplot].Divide(hlist2)
        #leg.AddEntry(hratio[iplot], legends, "p")
        #leg.AddEntry(hlist[iplot], legends[iplot], "p")
        #hlist[iplot].Draw("p,hist,same")
        hratio[iplot].SetMarkerSize(plottingStuff['markersize'])
        hratio[iplot].SetMarkerStyle(20)
        hratio[iplot].SetMarkerColor(r.kBlue)
        hratio[iplot].Draw("p,hist" + (iplot != 0) * "same")
        #hlist2[iplot].Draw("p,hist" + (iplot != 0) * "same")

    ilabel = 1
    
    for ich in range(4):
        for iwh in range(-2, 3):
     #       print (hratio[0].GetBinContent( iwh + 2 + 1 + 5 * ich ) )
            hratio[0].GetXaxis().ChangeLabel(ilabel, -1, -1, -1, -1, -1, (iwh > 0) * "+" + str(iwh))
            ilabel += 1
    #leg.Draw()

    textlist = []
    linelist = []
    for ich in range(4):
        textlist.append(r.TText(.17 + ich * 0.1975, 0.30, chambTag[ich]))
        textlist[-1].SetNDC(True)
        textlist[-1].Draw("same")
        if ich != 3:
            linelist.append(r.TLine(0.3075 + ich * 0.1975, 0.1, 0.3075 + ich * 0.1975, 0.9))
            linelist[-1].SetNDC(True)
            linelist[-1].Draw("same")

    firsttex = r.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{       CMS} Phase-2 Simulation")
    firsttex.Draw("same");

    secondtext = r.TLatex()
    toDisplay = r.TString()
    if (lookForPU(fil) != -1) : toDisplay  = r.TString("14 TeV, " + str(lookForPU(fil))  +" PU")
    else : toDisplay  = r.TString("14 TeV")
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
    secondtext.Draw("same")
    
    r.TGaxis.SetMaxDigits(4)
    r.gPad.Update()
    c.Update()

    savescaffold = 'hDividedRatio' 
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".png")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".pdf")
    c.SaveAs(path + "/" + savescaffold + str(binToUse+1) + ".root")
    c.Close(); del c
    return

















if __name__ == '__main__':
  main()



#def justMergePlots (file1, file2, plotscaffold, savescaffold, pathToSave, legends, plottingStuff):
     
#    plot1.

#    leg.addentry(, legends[iplot], "p")
#     hlist[iplot].draw("p,hist" + (iplot != 0) * "same")

#    leg.draw()


