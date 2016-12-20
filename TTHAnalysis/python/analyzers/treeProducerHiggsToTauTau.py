

from CMGTools.TTHAnalysis.analyzers.treeProducerHiggsCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

higgsToTauTau_globalVariables = higgsCore_globalVariables + [

            ##-------- custom jets ------------------------------------------
#JB            NTupleVariable("htJet25", lambda ev : ev.htJet25, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
#            NTupleVariable("metsig00", lambda ev : ev.mvaMetSig00, help="MET significance matrix(0,0)"),
#            NTupleVariable("metsig01", lambda ev : ev.mvaMetSig01, help="MET significance matrix(0,1)"),
#            NTupleVariable("metsig10", lambda ev : ev.mvaMetSig10, help="MET significance matrix(1,0)"),
#            NTupleVariable("metsig11", lambda ev : ev.mvaMetSig00, help="MET significance matrix(1,1)"),
#            NTupleVariable("svfitMass", lambda ev : ev.svfitMass, help="SVFit mass"),
#            NTupleVariable("svfitMassError", lambda ev : ev.svfitMassError, help="SVFit mass uncertainty"),
#            NTupleVariable("svfitPt", lambda ev : ev.svfitPt, help="SVFit pt"),

#MF            NTupleVariable("v_metsig00", lambda ev : ev.v_mvaMetSig00, help="MET significance matrix(0,0)"),

            
#            NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
#            NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("htJet40ja", lambda ev : ev.htJet40ja, help="H_{T} computed from only jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("htJet40", lambda ev : ev.htJet40, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("htJet40a", lambda ev : ev.htJet40a, help="H_{T} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("mhtJet40a", lambda ev : ev.mhtJet40a, help="H_{T}^{miss} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("nSoftBJetLoose25",  lambda ev: sum([(sv.mva>0.3 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with loose sv mva"),
#            NTupleVariable("nSoftBJetMedium25", lambda ev: sum([(sv.mva>0.7 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with medium sv mva"),
#            NTupleVariable("nSoftBJetTight25",  lambda ev: sum([(sv.mva>0.9 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with tight sv mva"),
            ##--------------------------------------------------
#            NTupleVariable("minMWjj", lambda ev: ev.minMWjj, int, help="minMWjj"),
#            NTupleVariable("minMWjjPt", lambda ev: ev.minMWjjPt, int, help="minMWjjPt"),
#            NTupleVariable("bestMWjj", lambda ev: ev.bestMWjj, int, help="bestMWjj"),
#            NTupleVariable("bestMWjjPt", lambda ev: ev.bestMWjjPt, int, help="bestMWjjPt"),
#            NTupleVariable("bestMTopHad", lambda ev: ev.bestMTopHad, int, help="bestMTopHad"),
#            NTupleVariable("bestMTopHadPt", lambda ev: ev.bestMTopHadPt, int, help="bestMTopHadPt"),
            ##--------------------------------------------------
            ##------------------------------------------------
]
higgsToTauTau_globalObjects = higgsCore_globalObjects.copy()
higgsToTauTau_globalObjects.update({
            # put more here
})

#higgsToTauTau_dileptons = higgsCore_dileptons.copy()

higgsToTauTau_collections = higgsCore_collections.copy()
higgsToTauTau_collections.update({

            # put more here
            "genJets"         : NTupleCollection("genJet", fourVectorType, 10, help="Generated jets (not cleaned)"),
            "genParticles"     : NTupleCollection("gen",  genParticleWithMotherId, 400, help="all pruned genparticles"), # need to decide which gen collection ?
            "generatorSummary"     : NTupleCollection("genSum",  genParticleWithLinksType, 400, help="all pruned genparticles"),
            #"gentaus"     : NTupleCollection("genTau",  genParticleWithLinksType, 200, help="all pruned genparticles"),
            ## ---------------------------------------------
#            "selectedLeptons" : NTupleCollection("LepGood", leptonTypeH, 8, help="Leptons after the preselection"),
            "selectedElectrons" : NTupleCollection("el", leptonTypeH, 20, help="Electrons after the preselection"),
            "selectedMuons" : NTupleCollection("mu", leptonTypeH, 20, help="Muons after the preselection"),
#            "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "selectedTaus"    : NTupleCollection("tau", tauTypeH, 20, help="Taus after the preselection"),
#            "selectedIsoTrack"    : NTupleCollection("track", isoTrackType, 50, help="isoTrack, sorted by pt"),
            ##------------------------------------------------
            "cleanJetsAll"       : NTupleCollection("jet",     jetTypeH, 100, help="Jets after full selection and cleaning, sorted by pt"),
#            "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusy, 25, help="Forward jets after full selection and cleaning, sorted by pt"),            
#mf            "fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
            #"reclusteredFatJets" : NTupleCollection("RCFatJet",     fourVectorType,20, help="FatJets reclusterd from ak4 cleanJetsAll"),
            ##------------------------------------------------
#mf            "ivf"       : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
#mf            "genBHadrons"  : NTupleCollection("GenBHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level B hadrons"),
#mf            "genDHadrons"  : NTupleCollection("GenDHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level D hadrons"),
            "dilepton"          : NTupleCollection("dilepton",     dileptonH, 1000, help="system of decay products of the two tau leptons"),
#ms            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),

            #"met" : NTupleCollection("met", metTypeH, help="PF E_{T}^{miss}, after type 1 corrections"),                             

            'TOE_IsoMu18' : NTupleCollection( 'triggerObject_IsoMu18', triggerObjectIsoMu18, 20 , help='trigger objects HLT_IsoMu18_v3'),
            'TOE_IsoMu20' : NTupleCollection( 'triggerObject_IsoMu20', triggerObjectIsoMu20, 20 , help='trigger objects HLT_IsoMu20_v4'),
            'TOE_IsoMu22' : NTupleCollection( 'triggerObject_IsoMu22', triggerObjectIsoMu22, 20 , help='trigger objects HLT_IsoMu22_v3'),
            'TOE_IsoMu22_eta2p1' : NTupleCollection( 'triggerObject_IsoMu22_eta2p1', triggerObjectIsoMu22_eta2p1, 20 , help='trigger objects HLT_IsoMu22_eta2p1_v2'),
            'TOE_IsoMu24' : NTupleCollection( 'triggerObject_IsoMu24', triggerObjectIsoMu24, 20 , help='trigger objects HLT_IsoMu24_v2'),
            'TOE_IsoMu27' : NTupleCollection( 'triggerObject_IsoMu27', triggerObjectIsoMu27, 20 , help='trigger objects HLT_IsoMu27_v4'),
            'TOE_IsoTkMu18' : NTupleCollection( 'triggerObject_IsoTkMu18', triggerObjectIsoTkMu18, 20 , help='trigger objects HLT_IsoTkMu18_v3'),
            'TOE_IsoTkMu20' : NTupleCollection( 'triggerObject_IsoTkMu20', triggerObjectIsoTkMu20, 20 , help='trigger objects HLT_IsoTkMu20_v5'),
            'TOE_IsoTkMu22' : NTupleCollection( 'triggerObject_IsoTkMu22', triggerObjectIsoTkMu22, 20 , help='trigger objects HLT_IsoTkMu22_v3'),
            'TOE_IsoTkMu22_eta2p1' : NTupleCollection( 'triggerObject_IsoTkMu22_eta2p1', triggerObjectIsoTkMu22_eta2p1, 20 , help='trigger objects HLT_IsoTkMu22_eta2p1_v2'),
            'TOE_IsoTkMu24' : NTupleCollection( 'triggerObject_IsoTkMu24', triggerObjectIsoTkMu24, 20 , help='trigger objects HLT_IsoTkMu24_v2'),
            'TOE_IsoTkMu27' : NTupleCollection( 'triggerObject_IsoTkMu27', triggerObjectIsoTkMu27, 20 , help='trigger objects HLT_IsoTkMu27_v4'),
            'TOE_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1', triggerObjectIsoMu17_eta2p1_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v5'),
            'TOE_IsoMu17_eta2p1_LooseIsoPFTau20' : NTupleCollection( 'triggerObject_IsoMu17_eta2p1_LooseIsoPFTau20', triggerObjectIsoMu17_eta2p1_LooseIsoPFTau20, 20 , help='trigger objects HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v5'),
            'TOE_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1', triggerObjectIsoMu19_eta2p1_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2'),
            'TOE_IsoMu19_eta2p1_LooseIsoPFTau20' : NTupleCollection( 'triggerObject_IsoMu19_eta2p1_LooseIsoPFTau20', triggerObjectIsoMu19_eta2p1_LooseIsoPFTau20, 20 , help='trigger objects HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2'),
            'TOE_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1', triggerObjectIsoMu21_eta2p1_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v2'),
            'TOE_Ele23_WPLoose_Gsf' : NTupleCollection( 'triggerObject_Ele23_WPLoose_Gsf', triggerObjectEle23_WPLoose_Gsf, 20 , help='trigger objects HLT_Ele23_WPLoose_Gsf_v4'),
            'TOE_Ele24_eta2p1_WPLoose_Gsf' : NTupleCollection( 'triggerObject_Ele24_eta2p1_WPLoose_Gsf', triggerObjectEle24_eta2p1_WPLoose_Gsf, 20 , help='trigger objects HLT_Ele24_eta2p1_WPLoose_Gsf_v2'),
            'TOE_Ele25_WPTight_Gsf' : NTupleCollection( 'triggerObject_Ele25_WPTight_Gsf', triggerObjectEle25_WPTight_Gsf, 20 , help='trigger objects HLT_Ele25_WPTight_Gsf_v2'),
            'TOE_Ele25_eta2p1_WPLoose_Gsf' : NTupleCollection( 'triggerObject_Ele25_eta2p1_WPLoose_Gsf', triggerObjectEle25_eta2p1_WPLoose_Gsf, 20 , help='trigger objects HLT_Ele25_eta2p1_WPLoose_Gsf_v2'),
            'TOE_Ele25_eta2p1_WPTight_Gsf' : NTupleCollection( 'triggerObject_Ele25_eta2p1_WPTight_Gsf', triggerObjectEle25_eta2p1_WPTight_Gsf, 20 , help='trigger objects HLT_Ele25_eta2p1_WPTight_Gsf_v2'),
            'TOE_Ele27_WPLoose_Gsf' : NTupleCollection( 'triggerObject_Ele27_WPLoose_Gsf', triggerObjectEle27_WPLoose_Gsf, 20 , help='trigger objects HLT_Ele27_WPLoose_Gsf_v2'),
            'TOE_Ele27_WPTight_Gsf' : NTupleCollection( 'triggerObject_Ele27_WPTight_Gsf', triggerObjectEle27_WPTight_Gsf, 20 , help='trigger objects HLT_Ele27_WPTight_Gsf_v2'),
            'TOE_Ele27_eta2p1_WPLoose_Gsf' : NTupleCollection( 'triggerObject_Ele27_eta2p1_WPLoose_Gsf', triggerObjectEle27_eta2p1_WPLoose_Gsf, 20 , help='trigger objects HLT_Ele27_eta2p1_WPLoose_Gsf_v3'),
            'TOE_Ele27_eta2p1_WPTight_Gsf' : NTupleCollection( 'triggerObject_Ele27_eta2p1_WPTight_Gsf', triggerObjectEle27_eta2p1_WPTight_Gsf, 20 , help='trigger objects HLT_Ele27_eta2p1_WPTight_Gsf_v3'),
            'TOE_Ele32_eta2p1_WPTight_Gsf' : NTupleCollection( 'triggerObject_Ele32_eta2p1_WPTight_Gsf', triggerObjectEle32_eta2p1_WPTight_Gsf, 20 , help='trigger objects HLT_Ele32_eta2p1_WPTight_Gsf_v3'),
            'TOE_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1', triggerObjectEle22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v3'),
            'TOE_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1', triggerObjectEle24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2'),
            'TOE_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20' : NTupleCollection( 'triggerObject_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20', triggerObjectEle24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20, 20 , help='trigger objects HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v2'),
            'TOE_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1', triggerObjectEle27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2'),
            'TOE_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1' : NTupleCollection( 'triggerObject_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1', triggerObjectEle32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1, 20 , help='trigger objects HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2'),
            'TOE_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg' : NTupleCollection( 'triggerObjectDoubleMediumIsoPFTau32_Trk1_eta2p1_Reg', triggerObjectDoubleMediumIsoPFTau32_Trk1_eta2p1_Reg, 20 , help='triggerObjectDoubleMediumIsoPFTau32_Trk1_eta2p1_Reg'),
            'TOE_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg' : NTupleCollection( 'triggerObjectDoubleMediumIsoPFTau35_Trk1_eta2p1_Reg', triggerObjectDoubleMediumIsoPFTau35_Trk1_eta2p1_Reg, 20 , help='triggerObjectDoubleMediumIsoPFTau35_Trk1_eta2p1_Reg'),
            'TOE_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg' : NTupleCollection( 'triggerObjectDoubleMediumIsoPFTau40_Trk1_eta2p1_Reg', triggerObjectDoubleMediumIsoPFTau40_Trk1_eta2p1_Reg, 20 , help='triggerObjectDoubleMediumIsoPFTau40_Trk1_eta2p1_Reg'),

            # "triggerObjectEvents_IsoMu17"            : NTupleCollection("triggerObject_IsoMu17",   triggerObjectIsoMu17, 20, help="trigger objects HLT_IsoMu17_eta2p1"),
            # "triggerObjectEvents_IsoMu18"            : NTupleCollection("triggerObject_IsoMu18",   triggerObjectIsoMu18, 20, help="trigger objects HLT_IsoMu18_v"),
            # "triggerObjectEvents_IsoMu24"            : NTupleCollection("triggerObject_IsoMu24",     triggerObjectIsoMu24, 20, help="trigger objects HLT_IsoMu24_eta2p1_v1"),
            # "triggerObjectEvents_IsoMu22"            : NTupleCollection("triggerObject_IsoMu22",     triggerObjectIsoMu24, 20, help="trigger objects HLT_IsoMu22_v1"),
            # "triggerObjectEvents_Ele22"            : NTupleCollection("triggerObject_Ele22",     triggerObjectEle22, 20, help="trigger objects HLT_Ele22_eta2p1_WP75_Gsf_LooseIsoPFTau20_v1"),
            # "triggerObjectEvents_Ele23"            : NTupleCollection("triggerObject_Ele23",     triggerObjectEle23, 20, help="trigger objects HLT_Ele23_WPLoose_Gsf_v*"),
            # "triggerObjectEvents_Ele32"            : NTupleCollection("triggerObject_Ele32",     triggerObjectEle32, 20, help="trigger objects HLT_Ele32_eta2p1_WP75_Gsf_v1"),           
            # "triggerObjectEvents_IsoPFTau35"            : NTupleCollection("triggerObject_IsoPFTau35",     triggerObjectIsoPFTau35, 20, help="trigger objects HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v2"),

            #"L1_DoubleIsoTau"            : NTupleCollection("L1_DoubleIsoTau",     L1_DoubleIsoTau, 20, help="L1 trigger objects"),

})



#Event.diLeptons[0].met().getSignificanceMatrix()(0,0)
 
