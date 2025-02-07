// ***************************************************************
// This file was created using the bat-project script
// for project TriProtonDecayAnalysis.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#include <BAT/BCLog.h>
#include "TriProtonDecay.h"
#include <TString.h>
#include <TFile.h>
#include <TTree.h>

int main(int argc, char *argv[])
{

    // TFile* inputFile = TFile::Open("../Input/testInput.root");
    // if(!inputFile){std::cout<<"Error opening input root file!"<<std::endl;}
    // TTree* inputTree = (TTree*)inputFile->Get("tree");
    // if(!inputTree){std::cout<<"Error opening input TTree!"<<std::endl;}

    //TFile* outputFile = new TFile("./Output/testOutput.root","RECREATE");
    //const char* outputFilePath = Form("../Output/modes_%d.root", injectedSignal);
    //TFile* outputFile = new TFile(outputFilePath,"RECREATE");
   
    const char* inputFilePath = argv[1];
    TFile* inputFile = TFile::Open(inputFilePath, "READ");

    TTree* inputTree = (TTree*)inputFile->Get("tree");
    int numEntries = inputTree->GetEntries();
    Long64_t nObserved = 0;
    Long64_t injectedSignal = 0;

    inputTree->SetBranchAddress("nObserved", &nObserved);
    inputTree->SetBranchAddress("injectedSignal", &injectedSignal);

    inputTree->GetEntry(0);
    
    const char* outputFilePath = Form("../Output/modes_%lld.root", injectedSignal);
    TFile* outputFile = new TFile(outputFilePath,"RECREATE");
    injectedSignal = 0;
    nObserved=0;
    
    TTree* modeTree = new TTree("tree","Tree containing modes");
    double npMode = 0.0;
    //int injectedSignal = -1;

    modeTree->Branch("npMode", &npMode);
    modeTree->Branch("injectedSignal", &injectedSignal); 

    // open log file
    BCLog::OpenLog("log.txt", BCLog::detail, BCLog::detail);

    // create new TriProtonDecay object
    //TriProtonDecay m("TriProtonDecay");

    // set precision
    //m.SetPrecision(BCEngineMCMC::kMedium);

    for(int it=0;it<numEntries;it++)
    {
        inputTree->GetEntry(it);
        TriProtonDecay* m = new TriProtonDecay("TriProtonDecay");
        m->SetPrecision(BCEngineMCMC::kMedium);
        m->SetNObs(nObserved);
        std::vector<double> modeVector;

        // run MCMC, marginalizing posterior
        m->MarginalizeAll(BCIntegrate::kMargMetropolis);

        // run mode finding; by default using Minuit
        modeVector = m->FindMode(m->GetBestFitParameters());
        npMode = modeVector[0];
        //injectedSignal = round(10*i);
        modeTree->Fill();
        npMode = -1;
        //injectedSignal = -1;

        //prepare prefixes for output files
        // const char* plotPath = Form("./Plots/");
        // const char* plotName = Form("_%d_plots_test.pdf",i);

        // const char* markovPath = "/pscratch/sd/v/vsharma2/TriNucleonDecay/MarkovChains/";
        // const char* markovName = Form("_%d_mcmc_test.root",i);

        // std::cout<<"!!!! \t"<<markovPath + m->GetSafeName() + markovName<<"\t !!!!"<<std::endl;

        //write Markov Chain to a ROOT file as a TTree
        //m->WriteMarkovChain(markovPath + m->GetSafeName() + markovName, "RECREATE", true, false);
        //m->WriteMarkovChain(markovPath + m->GetSafeName() + markovName, "RECREATE", true, true);
        //m->WriteMarkovChain(true);
        //m->WriteMarkovChain("mcmcfile.root","RECREATE");
        
        //draw all marginalized distributions into a PDF file
        //m->PrintAllMarginalized(m->GetSafeName() + "_plots.pdf");
        //m->PrintAllMarginalized(plotPath + m->GetSafeName() + plotName);
        delete m;
    }

    inputFile->Close();

    outputFile->cd();
    //const char* outputFilePath = Form("./Output/modes_%d.root", injectedSignal);
    //TFile* outputFile = new TFile(outputFilePath,"RECREATE");
    modeTree->Write();
    outputFile->Close();

    //BCLog::OutSummary("Test model created");

    //////////////////////////////
    // perform your analysis here

    // Normalize the posterior by integrating it over the full parameter space
    // m.Normalize();

    // Write Markov Chain to a ROOT file as a TTree
    // m.WriteMarkovChain(m.GetSafeName() + "_mcmc.root", "RECREATE");

    // run MCMC, marginalizing posterior
    //m.MarginalizeAll(BCIntegrate::kMargMetropolis);

    // run mode finding; by default using Minuit
    //m.FindMode(m.GetBestFitParameters());

    // draw all marginalized distributions into a PDF file
    //m.PrintAllMarginalized(m.GetSafeName() + "_plots.pdf");

    // print summary plots
    // m.PrintParameterPlot(m.GetSafeName() + "_parameters.pdf");
    // m.PrintCorrelationPlot(m.GetSafeName() + "_correlation.pdf");
    // m.PrintCorrelationMatrix(m.GetSafeName() + "_correlationMatrix.pdf");
    // m.PrintKnowledgeUpdatePlots(m.GetSafeName() + "_update.pdf");

    // print results of the analysis into a text file
    //m.PrintSummary();

    // close log file
    BCLog::OutSummary("Exiting");
    BCLog::CloseLog();

    return 0;
}
