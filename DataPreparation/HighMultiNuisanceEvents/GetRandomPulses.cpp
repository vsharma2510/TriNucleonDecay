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

int main(int argc, char **argv)
{
  string inputFileName = argv[1]; // Input file containing list of event numbers
  //TString prodFilePath = argv[3]; //Path to production files relevant to the run number
  //Extracting run number from file name
  size_t lastDot = inputFileName.find_last_of(".");
  size_t lastSlash = inputFileName.find_last_of("/");
  TString nameOnly = inputFileName.substr(lastSlash+1, lastDot-lastSlash-1);
  int runNumber = nameOnly.Atoi();
  int numRandEvents = 26088;

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
  TString outFileName = Form("./OutputFiles/%d_random.csv", runNumber);
  outputFile.open(outFileName.Data());
  outputFile<<"run"<<","<<"channel"<<","<<"time"<<","<<"energy"<<","<<"isSignal"<<","<<"isPulser"<<","<<"rejectBadIntervals"<<","
  <<"badForAnalysis"<<","<<"singleTrigger"<<","<<"numberOfPulses"<<","<<"timeStamp"<<","<<"riseTime"<<","<<"decayTime"<<"\n";

  // Getting list of event times and channels
  //vector<double> content = GetEvents(inputFile);

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
  double timeStamp = 0;

  //Cuore::QVector* sampleVector;
  double treeEventTime = 0;
  double treeEventDelay = 0;
  //int treeEventNumber = 0;
  int numEntries = qC->GetEntries();

  cout<<"Number of entries are "<<numEntries<<endl;

  int nImages=0;
  // Looping over raw data file
  cout<<"Looping over data file"<<endl;
  for(int e=0;e<numEntries;e++)
    {
        if(nImages==numRandEvents){break;}
        qC->GetEntry(e);
        treeEventTime = (header->GetTime().GetFromStartRunNs())/1e9;
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
        if(isSignal && rejectBadIntervals && badForAnalysis && singleTrigger && numberOfPulses==1 && !isPulser)
            {
                int random= rand() % 10 + 1;
                if(random > 5){continue;}
                if(random < 5){outputFile<<runNumber<<","<<treeChannel<<","<<adjustedTime<<","<<Energy<<","<<(int)isSignal<<","<<(int)isPulser<<","<<(int)rejectBadIntervals<<","<<(int)badForAnalysis<<","<<(int)singleTrigger<<","<<numberOfPulses<<","<<timeStamp<<","<<basicRiseTime<<","<<basicDecayTime<<"\n";
                nImages++;}
            }
	}
  outputFile.close();
  return 0;
}

