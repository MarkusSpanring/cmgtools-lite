import copy

common = [
    # 'drop *',
    'keep double_fixedGridRho*_*_*',
    'keep edmTriggerResults_TriggerResults_*_*',
    'keep patPackedTriggerPrescales_*_*_*',
    'keep patElectrons_slimmedElectrons_*_*',
    'keep patJets_slimmedJets_*_*',
    #'keep *_*_*_MVAMET',
    'keep patJets_patJetsReapplyJEC_*_*',
    'keep patMETs_slimmedMETs_*_*',
    'keep patMuons_slimmedMuons_*_*',
    # 'keep patPacked*_*_*_*',
    'keep patPackedCandidate*_*packedPFCandidates*_*_*', # RIC: agreed to keep it to: 1. tau vtx 2. possibly compute isolations at analysis level
    'keep *_*packedPFCandidates*_*_*',
    'keep patTaus_slimmedTaus_*_*',
    'keep patTrigger*_*_*_*',
    'keep *_offlineSlimmedPrimaryVertices_*_*',
##    'keep recoVertexs_*_*_*',
    'keep cmgMETSignificances_*_*_*',
    'keep patCompositeCandidates_cmg*CorSVFitFullSel_*_MVAMET',
    'keep patJets_patJetsAK4PF_*_*',
    'keep PileupSummaryInfos_*_*_*',
    'keep recoGenParticles_prunedGenParticles_*_*',
    'keep patPackedGenParticles_packedGenParticles__*', # these are status 1
    'keep recoGsfElectronCores_*_*_*', # needed?
    'keep recoSuperClusters_*_*_*', # for electron MVA ID
    'keep recoGenJets_slimmedGenJets_*_*',
    'keep *_slimmedSecondaryVertices_*_*',
    'keep patPackedCandidates_packedPFCandidates__*',
    'keep *_puppi_*_*',
    'keep *_slimmedMETsPuppi_*_*',
    'keep *_generator_*_*',
    'keep *_genEvtWeightsCounter_*_MVAMET',
    'keep *_offlineBeamSpot_*_*',
    'keep recoCaloClusters_*_*_*',
    'keep *_reducedEgamma_reducedConversions_*',
    'keep LHEEventProduct_externalLHEProducer_*_*',
    'keep *_l1extraParticles_*_*',
    'keep LHEEventProduct_*_*_*',
    'keep *_slimmedMETsNoHF_*_*',
    'keep *_patPFMet_*_*',
    'keep *_MVAMET_*_*',
    'keep *_patPFMetT1_*_*',
    'keep *_patPFMetT1JetResDown_*_*',
    'keep *_patPFMetT1JetResUp_*_*',
    'keep *_patPFMetT1Smear_*_*',
    'keep *_patPFMetT1SmearJetResDown_*_*',
    'keep *_patPFMetT1SmearJetResUp_*_*',
    'keep *_patPFMetT1Puppi_*_*',
    'keep *_slimmedMETsPuppi_*_*',
#    'keep *_offlinePrimaryVertices_*_*',
#    'keep *_selectedPrimaryVertexHighestPtTrackSumForPFMEtCorrType0_*_*',    
#    'keep patMETs_*_*_*',
#    'keep *_caloStage2Digis_*_*',
 #   'keep *_selectedPatTrigger_*_*'
    ]

commonDebug = copy.deepcopy(common) 
commonDebug.extend([
    'keep patCompositeCandidates_*_*_*', # keep all intermediate di-taus
    'keep patElectrons_*_*_*'
    ])
