#Configuration file fragment used for diLeptonFilter module (/plugins/diLeptonFilter.cc) initalisation

import FWCore.ParameterSet.Config as cms

eventDiLeptonFilter = cms.EDFilter("diLeptonSelector",
   srcTau = cms.InputTag("slimmedTaus"),
   tauPtCut = cms.double(18.0), 
   tauPtHardCut = cms.double(38.0),                                 
   tauEtaCut = cms.double(2.5),
   srcMuon = cms.InputTag("slimmedMuons"),
   muonPtCut = cms.double(18.0), 
   muonEtaCut = cms.double(2.5),
   srcElectron = cms.InputTag("slimmedElectrons"),
   electronPtCut = cms.double(20.0), 
   electronEtaCut = cms.double(2.5),
)
