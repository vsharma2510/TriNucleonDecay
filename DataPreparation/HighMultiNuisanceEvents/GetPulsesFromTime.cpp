//********************************************************************************************
//
// Macro to get raw pulses based on event numbers for a particular run
// Command line inputs
// 1) Input file named as "run_number.txt"
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
#include "QPulseInfo.hh"
#include "QVector.hh"
#include "QHeader.hh"
#include "QBaseType.hh"
#include "QObject.hh"
#include "QBool.hh"
#include "QOFData.hh"
#include "QTree.hh"
#include "QCountPulsesData.hh"
#include "QPulseParameters.hh"

using namespace std;
using namespace Cuore;

vector<double> GetEvents(TString filename)
{
  vector<double> content;
  //vector<string> row;
  //string line, word;
  double time;
  ifstream file(filename);
  //Opening input file
  if(file.is_open())
    {
      while (file >> time)
	    {
	    //Saving event number to file
	    content.push_back(time);
	    }
    }
  else
    {
    cout<<"Could not open the file\n"<<endl;
    }
  file.close();
  return content;
}

vector<vector<string> > GetEventChannelPair(TString filename)
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
    cout<<"Could not open the input file\n"<<endl;

  return content;
}

int main(int argc, char **argv)
{ 
  string inputFileName = argv[1]; // Input file containing list of event numbers
  //TString prodFilePath = argv[3]; //Path to production files relevant to the run number
  //Extracting run number from file name
  size_t lastDot = inputFileName.find_last_of(".");
  size_t lastSlash = inputFileName.find_last_of("/");
  TString nameOnly = inputFileName.substr(lastSlash+1, lastDot-lastSlash-1);
  int runNumber = nameOnly.Atoi();

  QDb::QDbTable table; 
  QCuoreDb *db = QCuoreDb::Get();
  TString tQuery = Form("select data_set from data_sets_runs where run_number=%d", runNumber);
  string query(tQuery.Data());
  db->DoQuery(query, table);
  QChain *qC = new QChain();

  if(!table["data_set"].empty()) 
    {
      for (int t=1;t<20;t++) 
        {
          string dataset = table["data_set"][0].GetString();
          cout<<"DATASET IS "<<dataset<<endl;
          TString filename = Form("/nfs/cuore7/data/CUORE/OfficialProcessed/ReproSpring20/output/ds%s/Production_%d_%03d_R.list", 
          dataset.c_str(), runNumber, t);
          //filename += "/" + table["filename"][i].GetString();
          cout<<"Adding "<<filename<<endl;
          int nAdded = qC->Add(filename.Data());
          if(!nAdded)
            {
              cout<<"Could not open production file for tower"<<t<<endl;
            }    
        }
    }    

  ofstream outputFile;
  TString outFileName = Form("./OutputFiles/%d_data.csv", runNumber);
  outputFile.open(outFileName.Data());
  outputFile<<"run"<<","<<"channel"<<","<<"time"<<","<<"eventNumber"<<","<<"groupNumber"<<","<<"energy"<<","<<"isSignal"<<","<<"isPulser"<<","<<"rejectBadIntervals"<<","
  <<"badForAnalysis"<<","<<"singleTrigger"<<","<<"numberOfPulses"<<","<<"timeStamp"<<","<<"riseTime"<<","<<"decayTime"<<","<<"delay"<<"\n";

  // Getting list of event times and channels
  //vector<double> content = GetEvents(inputFile);
  std::vector<vector<string> > content = GetEventChannelPair(inputFileName);

  qC->SetBranchStatus("*", 0);
  qC->SetBranchStatus("DAQ@Pulse.*", 1);
  qC->SetBranchStatus("DAQ@PulseInfo.*", 1);
  qC->SetBranchStatus("DAQ@Header*", 1);
  qC->SetBranchStatus("FilteredPulseAmplitude_wOF@OFData.*", 1);
  qC->SetBranchStatus("ApplySelectedEnergy@SelectedEnergy.*", 1);
  qC->SetBranchStatus("RejectBadIntervals@Passed.*", 1);
  qC->SetBranchStatus("SampleInfoFilter@Passed.*", 1);
  qC->SetBranchStatus("BadForAnalysis_GoodForAnalysis@Passed.*", 1);
  qC->SetBranchStatus("BCountPulses@CountPulsesData.*", 1);
  qC->SetBranchStatus("PulseBasicParameters@Parameters.*", 1);

  // Accessing QTree
  QPulse* pulse = new QPulse;
  qC->SetBranchAddress("DAQ@Pulse.", &pulse);
  QPulseInfo* pulseInfo = 0;
  qC->SetBranchAddress("DAQ@PulseInfo.", &pulseInfo);
  QHeader* header = 0;
  qC->SetBranchAddress("DAQ@Header.", &header);
  QOFData* of = 0;
  qC->SetBranchAddress("FilteredPulseAmplitude_wOF@OFData.", &of);
  QBaseType<double>* energy = 0;
  double Energy = 0;
  qC->SetBranchAddress("ApplySelectedEnergy@SelectedEnergy.", &energy);
  QBool* rbi = 0;
  bool rejectBadIntervals = false;
  qC->SetBranchAddress("RejectBadIntervals@Passed.", &rbi);
  QBool* st = 0;
  bool singleTrigger = false;
  qC->SetBranchAddress("SampleInfoFilter@Passed.", &st);
  QBool* bfa = 0;
  bool badForAnalysis = false;
  qC->SetBranchAddress("BadForAnalysis_GoodForAnalysis@Passed.", &bfa);
  QCountPulsesData* count = 0;
  int numberOfPulses = 0;
  qC->SetBranchAddress("BCountPulses@CountPulsesData.", &count);
  QPulseParameters* pbp = 0;
  double basicRiseTime, basicDecayTime = 0;
  qC->SetBranchAddress("PulseBasicParameters@Parameters.", &pbp);

  bool isSignal = false;
  bool isPulser = false;
  int treeChannel = 0;

  //Cuore::QVector* sampleVector;
  double treeEventTime = 0;
  double treeEventDelay = 0;
  int treeEventNumber = 0;
  //int treeEventNumber = 0;
  int numEntries = qC->GetEntries();

  cout<<"Number of entries are "<<numEntries<<endl;

  int nImages=0;
  // Looping over raw data file
  cout<<"Looping over data file"<<endl;
  for(int e=0;e<numEntries;e++)
    {
      if(nImages==(int)content.size()){break;}
      qC->GetEntry(e);
      treeEventTime = (header->GetTime().GetFromStartRunNs())/1e9;
      treeEventNumber = header->GetEventNumber(); 
      treeEventDelay = (of->GetDelay())/1e3;
      double adjustedTime = treeEventTime + treeEventDelay;
      isPulser = pulseInfo->GetMasterSample().GetIsStabPulser();
      isSignal =pulseInfo->GetMasterSample().GetIsSignal();
      Energy = (double)(*energy);
      rejectBadIntervals = (bool)(*bfa);
      badForAnalysis = (bool)(*bfa);
      singleTrigger = (bool)(*st);
      numberOfPulses = count->GetNumberOfPulses();
      treeChannel = pulseInfo->GetChannelId();
      basicRiseTime = pbp->fRiseTime;
      basicDecayTime = pbp->fDecayTime;

      //if (treeChannel == 764 && treeEventTime>8999.0 && treeEventTime <9300){cout<<"Channel 764 "<<adjustedTime<<endl;}
      //if(e%10000==0){cout<<channel<<" "<<treeEventTime<<endl;}
      //if(e%10000==0){cout<<"Looking at event "<<treeEventNumber<<endl;}
      
      // Looping over event times from input file
      //cout<<"Looping over text file"<<endl;
      for(std::vector<vector<string> >::iterator it = content.begin(); it != content.end(); ++it)
	      {
	        //double eventTime = (*it);
          TString timeS = (*it)[0];
          TString channelS = (*it)[1];
          TString timeStamp = (*it)[2];
          TString groupN = (*it)[3];
          double eventTime = timeS.Atof();
          int channel = channelS.Atoi();
          int groupNumber = groupN.Atoi();
		      //cout<<"Looking at event time "<<eventTime<<" and channel "<<channel<<endl;
	        if(abs(eventTime - adjustedTime) < 0.2 && channel == treeChannel) 
	          {
              outputFile<<runNumber<<","<<channel<<","<<adjustedTime<<","<<treeEventNumber<<","<<groupNumber<<","<<Energy<<","<<(int)isSignal<<","<<(int)isPulser<<","<<(int)rejectBadIntervals<<","
              <<(int)badForAnalysis<<","<<(int)singleTrigger<<","<<numberOfPulses<<","<<timeStamp<<","<<basicRiseTime<<","<<basicDecayTime<<","<<treeEventDelay<<"\n";
              nImages++;
              cout<<nImages<<"/"<<(int)content.size()<<endl;
              //outputFile<<adjustedTime<<","<<Energy<<","<<","<<(int)rejectBadIntervals<<","<<(int)badForAnalysis<<","<<(int)singleTrigger<<","<<numberOfPulses<<"\n";
	            /*
              Cuore::QVector sampleVector = pulse->GetSamples();
	            if(sampleVector.Size()==0)
		            {
		              cout<<"Event with time"<<eventTime<<" and channel "<<treeChannel<<" contains no pulse"<<endl;
		              continue;
		            }
	            // Drawing pulse
              
	            TCanvas* can = new TCanvas("c1","c1", 700,500);
	            TGraph* gr = sampleVector.GetGraph();
	            TString grTitle = Form("Run number %d, Channel %d, Event time %f", runNumber, channel, eventTime);
	            TString outFileName = Form("./PulsePlots/Run%d_Channel%d_Time%f.png", runNumber, channel, eventTime);
	            gr->SetTitle(grTitle);
	            gr->GetXaxis()->SetTitle("Time [ms]");
	            //->GetYaxis()->SetTitle()
	            gr->Draw("AL");
	            cout<<"Saving pulse image"<<endl;
	            can->SaveAs(outFileName);
	            pulse->Clear();
	            nImages++;
              */
	          }
	      }
    }
  outputFile.close();
  return 0;
}

