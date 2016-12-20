##########################################################
##       CONFIGURATION FOR Higgs->tautau TREES          ##
## skim condition: >= 0 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.higgsCore_modules_cff import * 

# Redefine what I need
lepAna.loose_muon_relIso = 999 #reliso03
lepAna.mu_isoCorr = "deltaBeta" 

lepAna.loose_electron_relIso = 999 #reliso03 
lepAna.ele_isoCorr = "deltaBeta" 

tauAna.tauLooseID = "decayModeFindingNewDMs"
tauAna.tauID = "decayModeFindingNewDMs"
tauAna.vetoLeptons = False
tauAna.vetoLeptonsPOG = False
tauAna.ptMin = 20
tauAna.etaMax = 2.5


jetAna.minLepPt = 10
jetAna.jetPt = 20
jetAna.jetEta = 4.7

jetAna.mcGT     = "Spring16_25nsV6_MC"
jetAna.dataGT   = "Fall15_25nsV2_DATA"
jetAna.do_mc_match = True
jetAna.smearJets = False #should be false in susycore, already                                      
jetAna.calculateSeparateCorrections = True 
jetAna.recalibrateJets =  True #For data  
jetAna.applyJetSmearing = False                                                                                                                                                        

metAna.recalibrate = False #should be false in susycore, already 
metAna.isDilepton=True
metAna.isTauMu=True
metAna.isTauEle=False

# --- LEPTON SKIMMING ---
#ttHLepSkim.minLeptons = 0
#ttHLepSkim.maxLeptons = 999
##LepSkim.idCut  = ""
##LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---

#ttHReclusterJets = cfg.Analyzer(
#            'ttHReclusterJetsAnalyzer',
#            )


## isoTrackAna.setOff=False

#from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer  import ttHReclusterJetsAnalyzer
#ttHReclusterJets = cfg.Analyzer(
#    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
#    )
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## Insert the SV analyzer in the sequence
#higgsCoreSequence.insert(higgsCoreSequence.index(ttHCoreEventAna),
#                        ttHFatJetAna)
#higgsCoreSequence.insert(higgsCoreSequence.index(ttHCoreEventAna),
#                        ttHSVAna)
#higgsCoreSequence.insert(higgsCoreSequence.index(ttHCoreEventAna),
#                        ttHHeavyFlavourHadronAna)



#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14  import *
#from CMGTools.RootTools.samples.samples_13TeV_74X_privat  import *

TriggerTag = 'HLT2'

triggerFlagsAna.processName = TriggerTag
triggerFlagsAna.triggerBits = {

 "IsoMu18"                                              : [ ''.join(["HLT_IsoMu18_v",str(i)])  for i in xrange(1,7)],
 "IsoMu20"                                              : [ ''.join(["HLT_IsoMu20_v",str(i)])  for i in xrange(1,7)],
 "IsoMu22"                                              : [ ''.join(["HLT_IsoMu22_v",str(i)])  for i in xrange(1,7)],
 "IsoMu22_eta2p1"                                       : [ ''.join(["HLT_IsoMu22_eta2p1_v",str(i)])  for i in xrange(1,7)],
 "IsoMu24"                                              : [ ''.join(["HLT_IsoMu24_v",str(i)])  for i in xrange(1,7)],
 "IsoMu27"                                              : [ ''.join(["HLT_IsoMu27_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu18"                                            : [ ''.join(["HLT_IsoTkMu18_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu20"                                            : [ ''.join(["HLT_IsoTkMu20_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu22"                                            : [ ''.join(["HLT_IsoTkMu22_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu22_eta2p1"                                     : [ ''.join(["HLT_IsoTkMu22_eta2p1_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu24"                                            : [ ''.join(["HLT_IsoTkMu24_v",str(i)])  for i in xrange(1,7)],
 "IsoTkMu27"                                            : [ ''.join(["HLT_IsoTkMu27_v",str(i)])  for i in xrange(1,7)],
 "IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1"              : [ ''.join(["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "IsoMu17_eta2p1_LooseIsoPFTau2"                        : [ ''.join(["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v",str(i)])  for i in xrange(1,7)],
 "IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"              : [ ''.join(["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "IsoMu19_eta2p1_LooseIsoPFTau2"                        : [ ''.join(["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",str(i)])  for i in xrange(1,7)],
 "IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1"              : [ ''.join(["HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "Ele23_WPLoose_Gsf"                                    : [ ''.join(["HLT_Ele23_WPLoose_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele24_eta2p1_WPLoose_Gsf"                             : [ ''.join(["HLT_Ele24_eta2p1_WPLoose_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele25_WPTight_Gsf"                                    : [ ''.join(["HLT_Ele25_WPTight_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele25_eta2p1_WPLoose_Gsf"                             : [ ''.join(["HLT_Ele25_eta2p1_WPLoose_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele25_eta2p1_WPTight_Gsf"                             : [ ''.join(["HLT_Ele25_eta2p1_WPTight_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele27_WPLoose_Gsf"                                    : [ ''.join(["HLT_Ele27_WPLoose_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele27_WPTight_Gsf"                                    : [ ''.join(["HLT_Ele27_WPTight_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele27_eta2p1_WPLoose_Gsf"                             : [ ''.join(["HLT_Ele27_eta2p1_WPLoose_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele27_eta2p1_WPTight_Gsf"                             : [ ''.join(["HLT_Ele27_eta2p1_WPTight_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele32_eta2p1_WPTight_Gsf"                             : [ ''.join(["HLT_Ele32_eta2p1_WPTight_Gsf_v",str(i)])  for i in xrange(1,7)],
 "Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    : [ ''.join(["HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    : [ ''.join(["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20"             : [ ''.join(["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v",str(i)])  for i in xrange(1,7)],
 "Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    : [ ''.join(["HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    : [ ''.join(["HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v",str(i)])  for i in xrange(1,7)],
 "DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg"               : [ ''.join(["HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v",str(i)])  for i in xrange(1,7)],
 "DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"               : [ ''.join(["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",str(i)])  for i in xrange(1,7)],
 "DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg"               : [ ''.join(["HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v",str(i)])  for i in xrange(1,7)]

}
triggerObjsAna.triggerResultsHandle = ('TriggerResults', '', TriggerTag)

triggerObjsAna.extraTrig = triggerFlagsAna.triggerBits["IsoMu18"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu20"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu22"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu22_eta2p1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu24"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu27"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu18"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu20"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu22"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu22_eta2p1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu24"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoTkMu27"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu17_eta2p1_LooseIsoPFTau2"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu19_eta2p1_LooseIsoPFTau2"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele23_WPLoose_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele24_eta2p1_WPLoose_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele25_WPTight_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele25_eta2p1_WPLoose_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele25_eta2p1_WPTight_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele27_WPLoose_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele27_WPTight_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele27_eta2p1_WPLoose_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele27_eta2p1_WPTight_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele32_eta2p1_WPTight_Gsf"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
triggerObjsAna.extraTrig += triggerFlagsAna.triggerBits["DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg"]

# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerHiggsToTauTau import *
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerHiggsToTauTau',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     PDFWeights = PDFWeights,
     PDFGen = PDFGen,
     globalVariables = higgsToTauTau_globalVariables,
     globalObjects = higgsToTauTau_globalObjects,
     collections = higgsToTauTau_collections,
)



#-------- SAMPLES AND TRIGGERS -----------

#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *

#from CMGTools.RootTools.samples.samples_13TeV_test import *
#print "Working"

#selectedComponents = [ SingleMu, DoubleElectron, TTHToWW_PUS14, DYJetsToLL_M50_PU20bx25, TTJets_PUS14 ]
#TTJets.splitFactor = 1000
#selectedComponents = [TTJets]

#selectedComponents = [QCD_HT_1000ToInf, QCD_HT_250To500, QCD_HT_500To1000, SMS_T1tttt_2J_mGl1200_mLSP800, SMS_T1tttt_2J_mGl1500_mLSP100, SMS_T2tt_2J_mStop425_mLSP325, SMS_T2tt_2J_mStop500_mLSP325, SMS_T2tt_2J_mStop650_mLSP325, SMS_T2tt_2J_mStop850_mLSP100, TBarToLeptons_sch, TBarToLeptons_tch, TBar_tWch, TTH, TTWJets, TTZJets, TToLeptons_sch, TToLeptons_tch, T_tWch]
#selectedComponents =WJetsToLNuHT +  [WJetsToLNu]  
##selectedComponents = DYJetsM50HT
##selectedComponents = MySamples 
#-------- SEQUENCE

#selectedComponents = HiggsSignalSamples

sequence = cfg.Sequence(
    higgsCoreSequence+[
#    ttHEventAna,
#    ttHReclusterJets,
    treeProducer,
    ])


#-------- HOW TO RUN
#test = 0
#selectedComponents = [ QCD_Pt_20toInf_MuEnriched15, QCD_Pt_20to30_MuEnrichedPt5, QCD_Pt_30to50_MuEnrichedPt5, QCD_Pt_50to80_MuEnrichedPt5, QCD_Pt_80to120_MuEnrichedPt5, QCD_Pt_120to170_MuEnrichedPt5, QCD_Pt_170to300_MuEnrichedPt5, QCD_Pt_300to470_MuEnrichedPt5 ]
#selectedComponents = [ TT_Fall2015_mt_160208 ]

#selectedComponents = [ DYJets_Fall2015_newMVAMet_160317 ]

selectedComponents = [ ]
#selectedComponents = [ DYJets_Fall2015_nlo_wo1step ]

#selectedComponents = [ DYJets_Fall2015_mt_amcatnloFXFX_160223_wo1step ]


# test = 3
# if test==1:
#     # test files XX-YY of first component                  
#     comp = XX_DSNAME_XX
#     comp.files = ['root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/jbrandst/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/SUSYGluGlu_miniAOD2_tauMu_151218/151218_143318/0000/tauMu_fullsel_tree_CMG_1.root']
#     print comp.files
#     selectedComponents = [comp]
#     comp.splitFactor = 250
#     comp.puFileData = 'MyDataPileupHistogram_observed_new.root'
#     comp.puFileMC = 'MyMCPileupHistogram_normOfficial.root'
# elif test==2:    
#     # test files XX-YY of first component                  
#     comp = SUSYGluGlu_mt_160203
#     comp.files = ['/data/jbrandstetter/CMGTools/76X/tauMu_fullsel_tree_CMG.root']
#     print comp.files
#     selectedComponents = [comp]
#     comp.splitFactor = 250
#     comp.puFileData = '../MyDataPileupHistogram_observed_new.root'
#     comp.puFileMC = '../MyMCPileupHistogram_normOfficial.root'
# elif test==3:
#     # test files XX-YY of first component
#     #comp = SUSYGluGlu_mt_160203
#     #comp = TT_Fall2015_mt_160208
#     for comp in selectedComponents:
#         comp.isMC=1
#         comp.isData=0
#         comp.splitFactor = 2500
#         comp.files = comp.files[:]
#         #selectedComponents = [comp]
#         comp.puFileData = "$CMSSW_BASE/src/CMGTools/RootTools/data/MyDataPileupHistogram_observed_new.root"
#         comp.puFileMC = "$CMSSW_BASE/src/CMGTools/RootTools/data/MyMCPileupHistogram_normOfficial.root"    

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     events_class = Events)
