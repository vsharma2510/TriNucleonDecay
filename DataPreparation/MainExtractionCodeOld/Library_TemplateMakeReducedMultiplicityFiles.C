#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

void MakeEventFiles( TString filename , TString outfilename, TString coincName , TString validName, Bool_t checkvalid = false )
{
/*Apr. 5, 2021
 * 
 * A quick macro to loop over a dataset etc. choosing specific multiplicity events & dump to reduced file
 */

    //output management: 
    
    Int_t multiplicityLow=MULTIPLICITYLOW;
    Int_t multiplicityHigh=MULTIPLICITYHIGH;
    
    
    TFile *outfile = new TFile(outfilename, "RECREATE");
    TTree *tree = new TTree("tree","Reduced CUORE data");
    if ( outfile->IsOpen() ) printf("Output File opened successfully\n");
    
    //input management:
    QChain *ch = new QChain();
    ch->Add( filename );
    TEventList eVList("eVList");

    std::ostringstream oss1;
    oss1<<multiplicityHigh;
    std::ostringstream oss2;
    oss2<<multiplicityLow;
    TString cutstr;
    cutstr+="((";
    cutstr+=coincName;
    cutstr+="@CoincidenceData.fMultiplicity<=";
    cutstr+=oss1.str();
//    cutstr+="))";
    cutstr+=") && (";
    cutstr+=coincName;
    cutstr+="@CoincidenceData.fMultiplicity>=";
    cutstr+=oss2.str();
    cutstr+=" ) && ( AnalysisBaseCut==1 )) ";

    std::cout<<"Cut String: "<<cutstr<<std::endl;
    ch->Draw(">>eVList",cutstr);
    std::cout<<"Num Drawn: "<<eVList.GetN()<<"/"<<ch->GetEntries()<<std::endl;
    
//    QPulse* pulse = 0;
    QHeader* header = 0;
    QPulseInfo* pulseinfo = 0;
    Double_t energy=0;
    Bool_t goodforanalysis=0;
    Bool_t noheaterinwindow=0;
    Int_t numberofpulses=0;
    Double_t of_delay=0;
    Bool_t rejectbadintervals=0;
    Bool_t singletrigger=0;
    QCoincidenceData* coincdata=0;
    Bool_t isvalid=0;
    Bool_t analysisbasecut=0;
    
    
//    ch->SetBranchAddress("DAQ@Pulse.",&pulse);
    ch->SetBranchAddress("DAQ@Header.",&header);
    ch->SetBranchAddress("DAQ@PulseInfo.",&pulseinfo);
    ch->SetBranchAddress("Energy",&energy);
    ch->SetBranchAddress("GoodForAnalysis",&goodforanalysis);
    ch->SetBranchAddress("NoHeaterInWindow",&noheaterinwindow);
    ch->SetBranchAddress("NumberOfPulses",&numberofpulses);
    ch->SetBranchAddress("OF_Delay",&of_delay);
    ch->SetBranchAddress("RejectBadIntervals",&rejectbadintervals);
    ch->SetBranchAddress("SingleTrigger",&singletrigger);
    ch->SetBranchAddress(coincName+"@CoincidenceData.",&coincdata);
    ch->SetBranchAddress(validName+"@Selected.fValue",&isvalid);
    ch->SetBranchAddress("AnalysisBaseCut",&analysisbasecut);
    //ch->SetBranchAddress(validName+"@Valid.fValue",&isvalid);
        
    Int_t nEvents = ch->GetEntries();
    
    //output handling...
    Double_t energies [MULTIPLICITYHIGH]={0.};
    Int_t channels [MULTIPLICITYHIGH]={0};
    Double_t times [MULTIPLICITYHIGH]={0};
    Double_t time=0;
    Int_t multiplicity=0;
    
    tree->Branch("Multiplicity",&multiplicity);
    tree->Branch("Time",&time);
    
    
    for(Int_t iN=0; iN<multiplicityHigh; iN++)
    {
        //Note this is a pretty cursed way to do this, but
        //root has abysmal support for writting things in a flexible way without
        //using a dictionary or a wrapper class or something
        //and I want this to be easily readable with uproot
        //Sorry for the shit variable declaration in a loop and horrible code practice!
        
        std::ostringstream oss;
        oss<<iN;
        //to_string doesn't seem to work :-(
        tree->Branch(("Channel"+oss.str()).c_str(),&channels[iN]);
        tree->Branch(("Energy"+oss.str()).c_str(),&energies[iN]);
        tree->Branch(("DeltaT"+oss.str()).c_str(),&times[iN]);
        
    }

    
    Int_t testcounter=0;
    for( Int_t iT=0; iT<eVList.GetN(); iT++)
    {
        //clear variables to make sure there's no weird leakage errors...
        std::fill(times,times+multiplicityHigh,0);
        std::fill(energies,energies+multiplicityHigh, 0.);
        std::fill(channels,channels+multiplicityHigh,0);
//         pulseinfo->Clear();
//         energy->Clear();
//         goodforanalysis->Clear();
//         noheaterinwindow->Clear();
//         numberofpulses->Clear();
//         of_delay->Clear();
//         rejectbadintervals->Clear();
//         singletrigger->Clear():
//         coincdata->Clear();
//         isvalid->Clear();


        ch->GetEvent( eVList.GetEntry( iT ) );
        
        if ( iT % 100000 == 0 )
        {
            std::cout<<iT<<"/"<<nEvents<<'\n';
        };
        
        //std::cout<<goodforanalysis<<noheaterinwindow<<numberofpulses<<rejectbadintervals<<singletrigger<<pulseinfo->GetIsSignal()<<std::cout;
        //some more cuts that can't really be passed at the "Draw" level...
        if ( checkvalid ){  if ( !isvalid ){continue;} } //currently set off, need to check how this works...
        if ( !goodforanalysis ){continue;}
        if ( !noheaterinwindow ){continue;}
        if ( numberofpulses != 1 ){continue;}
        if ( !rejectbadintervals ){continue;}
        if ( !singletrigger ){continue;}
        if ( pulseinfo->GetIsNoise() != 0 ){continue;}
        if ( pulseinfo->GetIsSide() != 0 ){continue;}
        if ( ! ( pulseinfo->GetIsSignal()==1 || pulseinfo->GetIsMuon()==1 ) ){continue;} //I don't think we actually use the muon flag, but better safe than sorry when looking for muons!
        if ( !analysisbasecut ){continue;}
        
        //deal with the first event & global parameters:
        multiplicity=coincdata->fMultiplicity;
        energies[0]=energy;
        //std::cout<<energies[0]<<std::endl;

        channels[0]=(pulseinfo->GetChannelId() );
        times[0]=of_delay/1000.;
        
        time=( header->GetTime().GetFromStartRunNs() )/1.e9;
        
        //std::cout<<multiplicity<<","<<coincdata->fOrderInMultiple<<std::endl;
        if( !(coincdata->fOrderInMultiple<=1) ){continue;}
        if ( multiplicity > 0 ):
        {
            //careful: touching any of the QMultiplicityData when in a M=1 event can be bad...
            for ( Int_t iM=0; iM < multiplicity - 1 ; iM++)
            {
                //indexing a little funny because of how QCoincidenceData is handled
                energies[iM+1]=coincdata->GetCoincidentChannel(iM).fEnergy;
                channels[iM+1]=coincdata->GetCoincidentChannel(iM).fChannelId;
                times[iM+1]=coincdata->GetCoincidentChannel(iM).fDeltaT;

            }

        }
        
        
        
        testcounter++;
        tree->Fill();
        //if ( testcounter > 100){break;}
        
        
    }
    
    std::cout<<testcounter<<" events written!"<<std::endl;
    
    
    outfile->Write();
    delete ch;
    std::cout<<"All done! :-)";
    

}
