import sys
from CMGTools.Production.datasetToSource import datasetToSource
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.tauTools import *
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET
from RecoMET.METPUSubtraction.jet_recorrections import loadLocalSqlite, recorrectJets

#from CMGTools.diLeptonSelector.diLeptonFilter_cfi.py import

process = cms.Process("MVAMET")
#process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(1000))
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))
numberOfFilesToProcess = -1

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v6'

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

#process.load('PhysicsTools.PatAlgos.slimming.unpackedTracksAndVertices_cfi')
#process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
#process.load('RecoBTag.Configuration.RecoBTag_cff')


dataset_user = 'CMS'
dataset_name = '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
dataset_files = '.*root'

process.source = datasetToSource(                                                                   
    dataset_user,
    dataset_name,
    dataset_files,
    )

# process.source = cms.Source("PoolSource",
#                             fileNames = cms.untracked.vstring("file:data.root")
#                           fileNames = cms.untracked.vstring("file:localTestFile.root")
#                           fileNames = cms.untracked.vstring("file:localTestFile_DY.root")
#                           )


isData=True
if not hasattr(process, "p"):                                                                                                                      
         process.p = cms.Path() 


process.load('CMGTools.diLeptonSelector.diLeptonFilter_cfi')
process.eventDiLeptonFilter
process.p *= (process.eventDiLeptonFilter) 

from CMGTools.H2TauTau.eventContent.common_cff import common

loadLocalSqlite(process, "Spring16_23Sep2016AllV2_DATA.db", tag = 'JetCorrectorParametersCollection_Spring16_23Sep2016AllV2_DATA_AK4PFchs') 

recorrectJets(process, isData)
jetCollection = "patJetsReapplyJEC"

# configure MVA MET
if isData:
    coll = "RECO"
else:
    coll = "PAT"

####################  correct MET ###############
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process,
                           isData = isData)

process.selectedVerticesForPFMEtCorrType0.src = cms.InputTag("offlineSlimmedPrimaryVertices")

process.load("RecoMET/METProducers.METSignificance_cfi")
process.load("RecoMET/METProducers.METSignificanceParams_cfi")

process.METCorrSignificance = process.METSignificance.clone(
 srcPfJets = cms.InputTag('patJetsReapplyJEC::MVAMET'),
 srcMet = cms.InputTag('slimmedMETs::MVAMET')
)

#################################################

runMVAMET( process, jetCollectionPF = jetCollection)
process.MVAMET.srcMETs = cms.VInputTag( cms.InputTag("slimmedMETs", "", coll),
                                             cms.InputTag("patpfMET"),
                                             cms.InputTag("patpfMETT1"),
                                             cms.InputTag("patpfTrackMET"),
                                             cms.InputTag("patpfNoPUMET"),
                                             cms.InputTag("patpfPUCorrectedMET"),
                                             cms.InputTag("patpfPUMET"),
                                             cms.InputTag("slimmedMETsPuppi", "", coll) )

process.MVAMET.srcPFCands =  cms.InputTag("packedPFCandidates")
process.MVAMET.srcLeptons  = cms.VInputTag("slimmedMuons", "slimmedElectrons", "slimmedTaus")
process.MVAMET.requireOS = cms.bool(False)


process.options = cms.untracked.PSet(
    allowUnscheduled=cms.untracked.bool(True)
)
process.source.inputCommands = cms.untracked.vstring(
    'keep *'
)
process.genEvtWeightsCounter = cms.EDProducer(
    'GenEvtWeightCounter',
    verbose = cms.untracked.bool(False)
)

######### correction of PU Jet Id ########### 
# process.load("RecoJets.JetProducers.PileupJetID_cfi")
# process.pileupJetIdUpdated = process.pileupJetId.clone(
#   jets=cms.InputTag("slimmedJets"),
#   inputIsCorrected=True,
#   applyJec=True,
#   vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")
#   )

# process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")
# process.patJetCorrFactorsReapplyJEC = process.updatedPatJetCorrFactors.clone(
#   src = cms.InputTag("slimmedJets"),
#   levels = ['L1FastJet', 'L2Relative', 'L3Absolute'] )
# process.updatedJets = process.updatedPatJets.clone(
#   jetSource = cms.InputTag("slimmedJets"),
#   jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
#   )
# process.updatedJets.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']

# process.p *= ( process.pileupJetIdUpdated + process.patJetCorrFactorsReapplyJEC + process.updatedJets )
#############################################


if not isData:
    process.genEvtWeightsCounterPath = cms.Path(process.genEvtWeightsCounter)
    #process.schedule.insert(0, process.genEvtWeightsCounterPath)

if numberOfFilesToProcess > 0:
    process.source.fileNames = process.source.fileNames[:numberOfFilesToProcess]


if isData:
    json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt'
    print json
## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10

#! Output and Log                                                                                                                                      
                                 
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName = cms.untracked.string('outfile_newMVA.root'),
                                  outputCommands = cms.untracked.vstring(common),
                                  SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p'))
                                  )

process.out = cms.EndPath(process.output)





