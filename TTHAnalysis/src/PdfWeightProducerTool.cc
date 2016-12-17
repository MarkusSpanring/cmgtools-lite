#include "CMGTools/TTHAnalysis/interface/PdfWeightProducerTool.h"
#include <cassert>

namespace LHAPDF {
      void initPDFSet(int nset, const std::string& filename, int member=0);
      int numberPDF(int nset);
      void usePDFMember(int nset, int member);
      double xfx(int nset, double x, double Q, int fl);
      double getXmin(int nset, int member);
      double getXmax(int nset, int member);
      double getQ2min(int nset, int member);
      double getQ2max(int nset, int member);
      void extrapolate(bool extrapolate=true);
}

void PdfWeightProducerTool::addPdfSet(const std::string &name) {
    pdfs_.push_back(name);
    weights_[name] = std::vector<double>();
}

//void PdfWeightProducerTool::beginJob(const LHERunInfoProduct & run) { //MF LHE
void PdfWeightProducerTool::beginJob() { //MF LHE
    for (unsigned int i = 0, n = pdfs_.size(); i < n; ++i) {
        LHAPDF::initPDFSet(i+1, pdfs_[i]);
    }

    exWeights_ = std::vector<double>();

    //MF LHE FROM HERE
    /*    
    int print_header = 0;
    if (print_header){

      typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;

      printf("LHE HEADER BEGIN\n");
      for (headers_const_iterator iter=run.headers_begin(); iter!=run.headers_end(); iter++){
	std::string m_s=iter->tag();
	printf("tag: %s \n", m_s.c_str() );
	std::vector<std::string> lines = iter->lines();
	for (unsigned int iLine = 0; iLine<lines.size(); iLine++) {
	  printf("%s\n", lines.at(iLine).c_str() );
	}
      }
      printf("LHE HEADER END\n");
    }
    */
    //MF LHE TILL HERE
}

//MF LHE complete method below
void PdfWeightProducerTool::extractWeight( const GenEventInfoProduct & pdfstuff , const LHEEventProduct & EvtHandle ) {

  //  printf("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW A\n");
  exWeights_.resize( EvtHandle.weights().size() );
  for (unsigned i=0; i<EvtHandle.weights().size(); i++) {
    //    if (EvtHandle.weights()[i].id == "YYY") theWeight *= EvtHandle.weights()[i].wgt/EvtHandle.originalXWGTUP(); 
    double theWeight = EvtHandle.weights()[i].wgt/EvtHandle.originalXWGTUP();
    std::string m_id=EvtHandle.weights()[i].id;
    //    printf("%i : %s : (%+8.4f)\n",i,m_id.c_str(),theWeight);
    std::vector<double> & exWeights = exWeights_;
    exWeights.at(i)=theWeight;
  }
  //  printf("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW B\n");

  /*
  printf("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS A\n");
  for (unsigned i=0; i<EvtHandle.scales().size(); i++) {
    double theWeight = EvtHandle.scales()[i];
    //  std::string m_id=EvtHandle.weights()[i].id;
    printf("%i : (%+8.4f)\n",i,theWeight);
  }
  printf("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS B\n");
  */

}

void PdfWeightProducerTool::processEvent(const GenEventInfoProduct & pdfstuff) {
  float Q = pdfstuff.pdf()->scalePDF;

  int id1 = pdfstuff.pdf()->id.first;
  if(std::abs(id1)==21) id1=0;
  double x1 = pdfstuff.pdf()->x.first;
  //  double t_pdf1 = pdfstuff.pdf()->xPDF.first; //mf

  int id2 = pdfstuff.pdf()->id.second;
  if(std::abs(id2)==21) id2=0;
  double x2 = pdfstuff.pdf()->x.second;
  //  double t_pdf2 = pdfstuff.pdf()->xPDF.second; //mf

  LHAPDF::usePDFMember(1,0);
  double pdf1 = LHAPDF::xfx(1, x1, Q, id1);
  double pdf2 = LHAPDF::xfx(1, x2, Q, id2);

  int print_pdfinfo = 0;

  if (print_pdfinfo){
    printf("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n");
    printf("pdf1: (%+8.4f), pdf2: (%+8.4f)\n",pdf1, pdf2);
    printf("Q: (%+8.4f)\n",Q);
    printf("id1: (%i)\n",id1);
    printf("x1: (%+8.4f)\n",x1);
    printf("id2: (%i)\n",id2);
    printf("x2: (%+8.4f)\n",x2);
    printf("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n");
  }

  for (unsigned int i = 0, n = pdfs_.size(); i < n; ++i) {
    std::vector<double> & weights = weights_[pdfs_[i]];
    unsigned int nweights = 1;
    if (LHAPDF::numberPDF(i+1)>1) nweights += LHAPDF::numberPDF(i+1);
    weights.resize(nweights);

    for (unsigned int j = 0; j < nweights; ++j) { 
      LHAPDF::usePDFMember(i+1,j);
      double newpdf1 = LHAPDF::xfx(i+1, x1, Q, id1);
      double newpdf2 = LHAPDF::xfx(i+1, x2, Q, id2);
      //printf("newpdf1: (%+8.4f), newpdf2: (%+8.4f)\n", newpdf1, newpdf2);
      weights[j] = (newpdf1/pdf1)*(newpdf2/pdf2);
      //printf("weight: (%+8.4f)\n", weights[j]);
    }
  }
}

const std::vector<double> & PdfWeightProducerTool::getWeights(const std::string &name) const {
    std::map<std::string, std::vector<double> >::const_iterator match = weights_.find(name);
    assert(match != weights_.end()); 
    return match->second;   
}

//MF LHE whole method
const std::vector<double> PdfWeightProducerTool::getExWeights(const std::string &name, const std::string &utype) const {
  std::vector<double> ret;
  for (unsigned i=0; i<exWeights_.size(); i++){
    //MADGRAPH LO SAMPLES
    if ( name == "MG" ){
      if ( utype == "pdf" ){
	if ( i>=10 && i<=109 ) ret.push_back( exWeights_.at(i) ); //9 is the nominal
      }
      if ( utype == "scale" ){
	if ( i<=8 ) ret.push_back( exWeights_.at(i) );
      }
    }
    //aMCatNLO samples
    if ( name == "aMC" ){
      if ( utype == "pdf" ){
	if ( i>=9 && i<=108 ) ret.push_back( exWeights_.at(i) );
      }
      if ( utype == "as" ){
	if ( i>=109 && i<=110 ) ret.push_back( exWeights_.at(i) );
      }
      if ( utype == "scale" ){
	if ( i<=8 ) ret.push_back( exWeights_.at(i) );
      }
    }

  }
  
  return ret;

}
