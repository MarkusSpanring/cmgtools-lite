// -*- C++ -*-
//
// Package:    CMGTools/diLeptonSelector
// Class:      diLeptonSelector
// 
/**\class diLeptonSelector diLeptonSelector.cc CMGTools/diLeptonSelector/plugins/diLeptonSelector.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Johannes Brandstetter
//         Created:  Fri, 11 Mar 2016 20:50:11 GMT
//
//


// system include files

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include <memory>
#include <vector>

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h" 
#include "DataFormats/Common/interface/Handle.h" 
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
//
// class declaration
//

class diLeptonSelector : public edm::stream::EDFilter<> {
   public:
      explicit diLeptonSelector(const edm::ParameterSet&);
      ~diLeptonSelector();

   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;

      // ----------member data ---------------------------
  edm::EDGetTokenT<pat::TauCollection> tokenTau_;
  edm::EDGetTokenT<pat::MuonCollection> tokenMuon_;
  edm::EDGetTokenT<pat::ElectronCollection> tokenElectron_;
  double tauPtCut_, tauPtHardCut_, tauEtaCut_;
  double muonPtCut_ , muonEtaCut_;
  double electronPtCut_, electronEtaCut_;
};

// constructor
diLeptonSelector::diLeptonSelector(const edm::ParameterSet& params):
  tokenTau_(consumes<pat::TauCollection>(params.getParameter<edm::InputTag>("srcTau"))),
  tokenMuon_(consumes<pat::MuonCollection>(params.getParameter<edm::InputTag>("srcMuon"))),
  tokenElectron_(consumes<pat::ElectronCollection>(params.getParameter<edm::InputTag>("srcElectron"))),
  tauPtCut_(params.getParameter<double>("tauPtCut")),
  tauPtHardCut_(params.getParameter<double>("tauPtHardCut")),
  tauEtaCut_(params.getParameter<double>("tauEtaCut")),
  muonPtCut_(params.getParameter<double>("muonPtCut")),
  muonEtaCut_(params.getParameter<double>("muonEtaCut")),
  electronPtCut_(params.getParameter<double>("electronPtCut")),
  electronEtaCut_(params.getParameter<double>("electronEtaCut"))
  
{}

// destructor
diLeptonSelector::~diLeptonSelector()
{
}

bool diLeptonSelector::filter(edm::Event& iEvent, const edm::EventSetup& params)
{
   using namespace edm;
   using namespace std;
   using namespace pat;

   edm::Handle<TauCollection> tauCollectionHandle;
   iEvent.getByToken(tokenTau_, tauCollectionHandle);
   const pat::TauCollection tauCollection = *(tauCollectionHandle.product());
   edm::Handle<MuonCollection> muonCollectionHandle;
   iEvent.getByToken(tokenMuon_, muonCollectionHandle);
   const pat::MuonCollection muonCollection = *(muonCollectionHandle.product());
   edm::Handle<ElectronCollection> electronCollectionHandle;
   iEvent.getByToken(tokenElectron_, electronCollectionHandle);
   const pat::ElectronCollection electronCollection = *(electronCollectionHandle.product());
   
   int counterSoftTaus = 0;
   int counterHardTaus = 0;
   int counterMuons = 0;
   int counterElectrons = 0;

   for (auto it : tauCollection)
     {    
       if(it.pt() > tauPtCut_ && abs(it.eta()) < tauEtaCut_) 
	 {
	   counterSoftTaus++;
	 }
       if(it.pt() > tauPtHardCut_ && abs(it.eta()) < tauEtaCut_) 
	 {
	   counterHardTaus++;
	 }
       
     }
   for (auto it : muonCollection)
     {    
       if(it.pt() > muonPtCut_ && abs(it.eta()) < muonEtaCut_) 
	 {
	   counterMuons++;
	 }
     }
   for (auto it : electronCollection)
     {    
       if(it.pt() > electronPtCut_ && abs(it.eta()) < electronEtaCut_) 
	 {
	   counterElectrons++;
	 }
     }
   
   if( counterHardTaus >= 2 ) return true;
   if( counterSoftTaus >=1 && counterMuons >=1 ) return true;
   if( counterMuons >=1 ) return true;
   if( counterSoftTaus >=1 && counterElectrons >=1 ) return true;

   return false;
}


//define this as a plug-in
DEFINE_FWK_MODULE(diLeptonSelector);
