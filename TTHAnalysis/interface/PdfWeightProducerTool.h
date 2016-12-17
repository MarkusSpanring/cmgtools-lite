#ifndef CMGTools_TTHAnalysis_PdfWeightProducerTool_h
#define CMGTools_TTHAnalysis_PdfWeightProducerTool_h

/// TAKEN FROM http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/ElectroWeakAnalysis/Utilities/src/PdfWeightProducer.cc?&view=markup

#include <string>
#include <vector>
#include <map>
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h" //MF LHE
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h" //MF LHE

class PdfWeightProducerTool {
    public:
        PdfWeightProducerTool() {}
        void addPdfSet(const std::string &name) ;
	//        void beginJob(const LHERunInfoProduct & run) ; //MF LHE
	void beginJob() ; //MF LHE
	void extractWeight( const GenEventInfoProduct & pdfstuff , const LHEEventProduct & EvtHandle ) ; //MF LHE
	const std::vector<double> getExWeights(const std::string &name, const std::string &utype) const ;
        void processEvent(const GenEventInfoProduct & pdfstuff ) ;
        const std::vector<double> & getWeights(const std::string &name) const ;
    private:
        std::vector<std::string> pdfs_;
        std::map<std::string, std::vector<double> > weights_;
        std::vector<double> exWeights_;
};

#endif
