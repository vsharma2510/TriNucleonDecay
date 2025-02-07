void PhaseSpace_2D() {
   if (!gROOT->GetClass("TGenPhaseSpace")) gSystem->Load("libPhysics");
   TLorentzVector W(0.0, 0.0, 0.0, 121.01);
   //TLorentzVector beam(0.0, 0.0, .65, .65);
   //TLorentzVector W = beam + target;
   //(Momentum, Energy units are Gev/C, GeV)
   Double_t masses[4] = { 118.22, 0.139, 0.139, 0.000511} ;
   TGenPhaseSpace event;
   event.SetDecay(W, 4, masses);
   TH2F *h2 = new TH2F("h2","h2", 50,0.0,3.0, 50,0.0,3.0);
   for (Int_t n=0;n<1000000;n++) {
      Double_t weight = event.Generate();
      TLorentzVector *pIn = event.GetDecay(0);
      TLorentzVector *pPip    = event.GetDecay(1);
      TLorentzVector *pPim    = event.GetDecay(2);
      TLorentzVector *ePim    = event.GetDecay(3);
      //TLorentzVector pPPip = *pProton + *pPip;
      //TLorentzVector pPPim = *pProton + *pPim;
      //std::cout<<(pPip->Gamma()-1)*0.139<<std::endl;
      h2->Fill((pPim->Gamma()-1)*0.139, (ePim->Gamma()-1)*0.000511 ,weight);
   }
   h2->Draw("COLZ");
}
