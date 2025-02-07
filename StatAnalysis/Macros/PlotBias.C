#include <TString.h>
#include <TFile.h>
#include <TTree.h>
#include <TF1.h>
#include <TGraph.h>
#include <TMath.h>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <vector>
#include <iostream>
#include <TMath.h>
using namespace std;
int main()
{

    std::vector<double> injectedSignal;
    std::vector<double> mean;
    std::vector<double> sd;
    //TFile* f=NULL;
    std::vector<double> npModeVector;

    for(int i=1; i<11; i++)
    {
        std::cout<<"Initializing npModeVector"<<std::endl;
//        std::vector<double> npModeVector;
        std::cout<<"Pushing back injectedSignal"<<std::endl;
        injectedSignal.push_back(i*10);
        std::cout<<"Adding file"<<std::endl;
        TString inputFile = Form("/global/homes/v/vsharma2/TriProtonDecay/StatAnalysis/Output/modes_%d.root", i*10);
        std::cout<<inputFile<<std::endl;
        std::cout<<"Read file"<<std::endl;
        // TFile* 
          TFile* f = new TFile(inputFile.Data(), "READ");
           if(f){f->ls();} 
  //  if(f){f->cd();}
    //    if(!f || !f->IsOpen()){cout<<"Problem with file "<<endl;; exit(0);}
    //    std::cout<<"Get tree"<<std::endl;
      //  TTree* tree = (TTree*)f->Get("tree");
        //double npMode = 0;
    //if(!tree){ cout<<"Problem with tree"<<endl; exit(0);}
        // std::vector<double> npModeVector = 0;
        // std::vector<double> mean = 0;
        // std::vector<double> sd = 0;
   /*     std::cout<<"Set branch"<<std::endl;
        tree->SetBranchAddress("npMode", &npMode);
        int numEntries = tree->GetEntries();

        std::cout<<"Filling vectors"<<std::endl;
        for(int it=0;it<numEntries;it++)
        {
            tree->GetEntry(it);
            npModeVector.push_back(npMode);
        }

 */
    f->Close();
/*
        mean.push_back(TMath::Mean(npModeVector.size(), &npModeVector[0]));
        sd.push_back(TMath::RMS(npModeVector.size(),  &npModeVector[0]));

        std::cout<<"Cleaning up vector"<<std::endl;
        npModeVector.clear();

        std::cout<<"Cleaning up f"<<std::endl;
        delete f;

        // std::cout<<"Cleaning up tree"<<std::endl;
        // delete tree;
        //std::cout<<"Cleaning up file"<<std::endl;
        //delete inputFile;
    
    */
        std::cout<<"End loop"<<std::endl;
    
    }
/*
    std::cout<<"Plotting"<<std::endl;
    TGraphErrors* graph = new TGraphErrors(injectedSignal.size(), &injectedSignal[0], &mean[0], 0, &sd[0]);
    //TGraphErrors* graph = new TGraphErrors(&injectedSignal, &mean, 0, &sd);
    TCanvas* canvas = new TCanvas("canvas", "Graph with Fit", 800, 600);
    graph->SetTitle("Graph with Fit");
    graph->SetMarkerStyle(20);
    graph->SetMarkerSize(1.0);
    graph->Draw("AP");

    TF1 *fitFunction = new TF1("fitFunction", "[0] + [1]*x", 0, graph->GetX()[graph->GetN()-1]);
    fitFunction->SetParameters(0,0.707);
    graph->Fit(fitFunction, "Q");
    fitFunction->Draw("same");

    canvas->Draw();

  */
   return 0;
}