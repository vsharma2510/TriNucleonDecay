{

  TCanvas* can = new TCanvas("c1", "c1", 700, 500);
  
  QChain* qC = new QChain("qtree");
  qC->Add("/global/cfs/cdirs/cuore/projecta/cuore/syncData/CUORE/RawData/run302047/QRaw_302407_B.list");
  QPulse* p = new QPulse;
  qC->SetBranchAddress("DAQ@Pulse.", &p);
  
  Cuore::QVector* sampleVector;
  for(int i=0;i<100;i++){
    qC->GetEntry(i);
    sampleVector = p->GetSamples();
    if(!sampleVector)continue;
    TGraph* gr = sampleVector->GetGraph();
    gr->Draw("AL");
    can->SaveAs("pulses_vivek.gif+50");
    p->Clear();
    int a = 0;
    gSystem->ProcessEvents();
    cout<<"Say 1 for go"<<endl;
    cin>>a;
  }
}
    
