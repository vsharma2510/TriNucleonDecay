//********************************************************************************************
//
// Macro to get raw pulses based on event numbers for a particular run
// Command line inputs
// 1) Run number
// 2) Path to text file containing event numbers 
// Compile as: g++ `diana-config --cflags --libs` GetPulsesFromRun.cpp -o GetPulsesFromRun 
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
#include <iomanip>
#include <cstdlib>

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
#include "QDb.hh"
#include "QCuoreDb.hh"
#include "QChain.hh"
#include "QPulse.hh"
#include "QVector.hh"
#include "QHeader.hh"

using namespace std;

vector<int> GetEvents(TString filename)
{
  
  vector<int> content;
  
  //vector<string> row;
  //string line, word;
  
  int number;
  ifstream file(filename);
  //Opening input file
  if(file.is_open())
    {
      while (file >> number)
	{
	  //Saving event number to file
	  content.push_back(number);
	}
    }
  else
    cout<<"Could not open the file\n"<<endl;

  file.close();
  return content;
}

int main(int argc, char **argv)
{
  int runNumber = atoi(argv[1]); 
  TString inputFile = argv[2]; // Input file containing list of event numbers
  
  // Getting paths of relevant QRaw files
  QDb::QDbTable table; 
  QCuoreDb *db = QCuoreDb::Get();
  TString tQuery = Form("select directory, filename from bookkeeping_ntuples where run_number=%d and hostname='ULITE'", runNumber);
  string query(tQuery.Data());
  db->DoQuery(query, table);
  TChain* qC = new TChain("qtree");

  if(!table["directory"].empty()) 
  {
    for (unsigned int i = 0; i < table["directory"].size(); ++i) 
    {
      std::string filename =  table["directory"][i].GetString();
      filename += "/" + table["filename"][i].GetString();
      cout<<"Adding "<<filename<<endl;
      int nAdded = qC->Add(filename.c_str());
      if(!nAdded)
        {
          cout<<"Could not open raw data file"<<endl;
        }    
    }
  }

  // Getting list of event numbers
  vector<int> content = GetEvents(inputFile);
  
  // Accessing QTree
  QPulse* p = new QPulse;
  qC->SetBranchAddress("DAQ@Pulse.", &p);
  QHeader* header = 0;
  qC->SetBranchAddress("DAQ@Header.", &header);
  //Cuore::QVector* sampleVector;
  int treeEventNumber = 0;
  int numEntries = qC->GetEntries();

  cout<<"Number of entries are "<<numEntries<<endl;

  int nImages=0;
  // Looping over raw data file
  cout<<"Looping over raw data file"<<endl;
  for(int e=0;e<numEntries;e++)
    {
      if(nImages==(int)content.size()){break;}
      qC->GetEntry(e);
      treeEventNumber = header->GetEventNumber();
      //if(e%10000==0){cout<<"Looking at event "<<treeEventNumber<<endl;}
      
      // Looping over event numbers from input file
      for(std::vector<int>::iterator it = content.begin(); it != content.end(); ++it)
	{
	  int eventNumber = (*it);
	  if(eventNumber == treeEventNumber)
	    {
	      Cuore::QVector sampleVector = p->GetSamples();
	      if(sampleVector.Size()==0)
		{
		  cout<<"Event number "<<eventNumber<<" contains no pulse"<<endl;
		  continue;
		}
	      // Drawing pulse
	      TCanvas* can = new TCanvas("c1","c1", 700,500);
	      TGraph* gr = sampleVector.GetGraph();
	      TString grTitle = Form("Run number %d -- Event number %d", runNumber, eventNumber);
	      TString outFileName = Form("Run%dEvent%d.png", runNumber, eventNumber);
	      gr->SetTitle(grTitle);
	      gr->GetXaxis()->SetTitle("Time [ms]");
	      //->GetYaxis()->SetTitle()
	      gr->Draw("AL");
	      cout<<Form("Saving pulse image for run %d and event %d", runNumber, eventNumber)<<endl;
	      can->SaveAs(outFileName);
	      p->Clear();
	      nImages++;
	    }
	}
    }
  return 0;
}

