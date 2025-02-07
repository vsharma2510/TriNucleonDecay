#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

void MakeEventFiles(const char * filename , const char * outfilename  )
{
    /* a root macro to pull all events from production-level files for lighter analysis
     *This version: Daniel Mayer dmayer@mit.edu, Oct. 26, 2021
     * 
     * 
     * 
     * 
     * 
     */
    
    //output management
    TFile *file = new TFile(outfilename, "RECREATE");
    TTree *tree = new TTree("tree","Reduced CUORE data");
    
    //input management
    QChain *ch = new QChain();
    ch->Add( filename );
    
    //variables to assign to tree branches
    QHeader* header = 0;
    QPulseInfo* pulseinfo = 0;
    QOFData* ofdata=0;    
    QCountPulsesData* countpulses=0;
    Cuore::QDouble* selectedenergy=0;
    Cuore::QDouble* stabamplitude=0;
    Cuore::QBool* noheaterinwindow=0;
    Cuore::QBool* rejectbadintervals=0;
    Cuore::QDouble* maxbaseline=0;
    QBaselineData* baseline=0;
    Cuore::QInt* maxposinwindow=0;
    
    //QChain branch assignment
    ch->SetBranchAddress("DAQ@Header.",&header);
    ch->SetBranchAddress("DAQ@PulseInfo.",&pulseinfo);
    ch->SetBranchAddress("FilteredPulseAmplitude@OFData.",&ofdata);
    ch->SetBranchAddress("BCountPulses@CountPulsesData.",&countpulses);
    ch->SetBranchAddress("ApplySelectedEnergy@SelectedEnergy.",&selectedenergy);
    ch->SetBranchAddress("CorrectAmplitudes_heaterTGS@Amplitude.",&stabamplitude);
    ch->SetBranchAddress("NoHeaterInWindow@Passed.",&noheaterinwindow);
    ch->SetBranchAddress("RejectBadIntervals@Passed.",&rejectbadintervals);
    ch->SetBranchAddress("PulseBasicParameters@MaxBaseline.",&maxbaseline);
    ch->SetBranchAddress("BaselineModule@BaselineData.",&baseline);
    ch->SetBranchAddress("PulseBasicParameters@MaxPosInWindow.",&maxposinwindow);
    


    Int_t nEvents = ch->GetEntries();
    std::cout<<"Number of Events:"<<nEvents<<'\n';
    
    //output variables
    ULong64_t time=0;
    Double_t Time=0.;
    UInt_t channel=0;
    UInt_t run=0;
    Double_t ofdelay=0.;
    Double_t ofrisetime=0.;
    UInt_t numpulses=0;
    Double_t selE=0.;
    Double_t stabA=0.;
    Double_t maxBaseline=0;
    Double_t Baseline=0;
    Double_t amplitude=0;
    Bool_t rejectBad=0;
    Bool_t noHeater=0;
    Bool_t isSig=0;
    Bool_t isPulser=0;
    Bool_t isNoise=0;
    Bool_t isMuon=0;
    Bool_t isSide=0;
    Int_t MaxPosInWindow=0;
    Int_t TempMaxPosInWindow=0;

    
    //output branch management
    tree->Branch("Channel",&channel);
    tree->Branch("Time",&Time);
    tree->Branch("NumPulses",&numpulses);
    tree->Branch("OFdelay",&ofdelay);
    tree->Branch("MaxPosInWindow",&MaxPosInWindow);
    tree->Branch("SelectedEnergy",&selE);
    tree->Branch("Baseline",&Baseline);
    tree->Branch("MaxToBaseline",&maxBaseline);
    tree->Branch("NoHeaterInWindow",&noHeater);
    tree->Branch("RejectBadIntervals",&rejectBad);
    tree->Branch("IsSignal",&isSig);
    tree->Branch("IsMuon",&isMuon);
    tree->Branch("IsPulser",&isPulser);
    tree->Branch("IsNoise",&isNoise);
    tree->Branch("IsSide",&isSide);


    for (Int_t iT=0; iT<nEvents; iT++)
    {
        //sometimes you need to clear things manually...
        maxbaseline->Clear();
        maxposinwindow->Clear();
        baseline->Clear();
        pulseinfo->Clear();
        ofdata->Clear();
        countpulses->Clear();
        selectedenergy->Clear();
        noheaterinwindow->Clear();
        rejectbadintervals->Clear();
        header->Clear();
        
        //just a little counter to keep track of numbers
        if ( iT % 100000 == 0 )
        {
            std::cout<<iT<<"/"<<nEvents<<'\n';
        };
        
        ch->GetEntry( iT );

        //check for event type; we'll throw out the noise & pulser
        isSig=(pulseinfo->GetIsSignal() );
        isPulser=(pulseinfo->GetIsPulser() );
        isNoise=(pulseinfo->GetIsNoise()) ;
        isMuon=(pulseinfo->GetIsMuon() );
        isSide=(pulseinfo->GetIsSide() );
        
        numpulses=countpulses->fNumberOfPulses;
        
        rejectBad=*rejectbadintervals;
        noHeater=*noheaterinwindow;
        selE=*selectedenergy;
        
        time=( header->GetTime().GetFromStartRunNs() );
        Time=time/1.e9;

        channel=(pulseinfo->GetChannelId() );
        ofdelay=ofdata->GetDelay()/1.e3;
        run=header->GetRun();
        
        maxBaseline=*maxbaseline;
        Baseline=baseline->GetBaseline();
        TempMaxPosInWindow=*maxposinwindow;
        MaxPosInWindow=TempMaxPosInWindow/1.e3;
        tree->Fill();
        
    };
    
    file->Write();
    
    
    delete ch;
    std::cout<<"All done! :-)";
    
}
