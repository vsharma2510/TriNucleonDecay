//********************************************************************************************
//
// Macro to get raw pulses based on event numbers or timestamps from CUORE production files.
// Command line inputs
// 1) Path to text file containing run number, event number pairs
// 2) Path to RawData directory corresponding to relevant run numbers
// Compile with -std=c++11
// author: Vivek Sharma
// date: 2023-02-23
//
// *******************************************************************************************

#include <iostream>
#include <fstream>
#include <getopt.h>
#include <vector>
#include <string>
#include <sstream>
#include <ostream>
//#include <iomanip>
//#include <cstdlib>

#include <TH2.h>
#include <TROOT.h>
#include <TCanvas.h>
#include <TString.h>
#include <TFile.h>
#include <TLegend.h>
#include <TF1.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include <TPad.h>
//#include <chrono>

#include "QChain.hh"
#include "QPulse.hh"
#include "QVector.hh"

using namespace std;

vector<vector<string> > GetRunEventPair(TString filename)
{
  
  vector<vector<string> > content;
  vector<string> row;
  string line, word;
  
  fstream file (filename, ios::in);
  if(file.is_open())
    {
      while(getline(file, line))
	    {
	      row.clear();	  
	      stringstream str(line);
	      while(getline(str, word, ','))
          {
	        row.push_back(word);
          }
	      content.push_back(row);
	    }
    }
  else
    cout<<"Could not open the file\n"<<endl;

  return content;
}

int main(int argc, char **argv)
{

  //  gSystem->Load("/cuore/soft/boost/stage/lib/libboost_thread.so");
  //  gSystem->Load("$CUORE_INSTALL/lib/libapollordcf.so");

  TString inputFile = argv[1];
  TString rawDataPath = argv[2];
  
  vector<vector<string> > content = GetRunEventPair(inputFile);
  
  TCanvas* can = new TCanvas("c1","c1", 700,500);
  
  for(std::vector<vector<string> >::iterator it = content.begin(); it != content.end(); ++it)
    {
      int runNumber = std::stoi((*it).at(0));
      TString runType = (*it).at(1);
      int eventNumber = std::stoi((*it).at(2));
      QChain* qC = new QChain("qtree");
      qC->Add(Form("%s/QRaw_%d_%s.list", rawDataPath.Data(), runNumber, runType.Data()));
      cout<<"Run number "<<runNumber<<" Run Type "<<runType<<" Event Number "<<eventNumber<<endl;
    }
  //QChain* qC = new QChain("qtree");
  //qC->Add("/nfs/cuore1/data/CUORE/RawData/run300658/QRaw_300658_T.list");
  
  
  QPulse* p = new QPulse;
  qC->SetBranchAddress("DAQ@Pulse.", &p);
  
  Cuore::QVector* sampleVector;//a holder for the actual samples of a pulse
  for(int i=0;i<100;i++){
    qC->GetEntry(i);
    sampleVector = p->GetSamples();
    if(!sampleVector)continue;
    TGraph* gr = sampleVector->GetGraph();
    gr->Draw("AL");
    can->SaveAs("pulses_vivek.gif+50");
    p->Clear();
    //cout<<*energy<<endl;
    //delete gr;
    int a =0;
    gSystem->ProcessEvents();
    cout<<"Say 1 for go"<<endl;
    cin>>a;
   
  }
  
  return 0;
}
