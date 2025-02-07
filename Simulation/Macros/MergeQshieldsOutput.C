{
    TFile* outFile = TFile::Open("TestPionSimTotal.root","RECREATE");
    outFile->cd();
    TChain q("qtree");
    cout<<"Adding qshields outputs"<<endl;
    q.Add("../Output/test_pion_sim_2000MeV_*.root");
    q.Merge("TestPionSimTotal.root");
    outFile->Close();
}