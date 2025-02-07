#include <BAT/BCLog.h>

#include "TriProtonDecay.h"

int main()
{
    //Open log file
    BCLog::OpenLog("log.txt", BCLog::detail, BCLog::detail);

    //Create new TriProtonDecayModel object
    TriProtonDecay m("TriProtonDecay");
    //Set precision
    m.SetPrecision(BCEngineMCMC::kMedium); //TODO:What precision?
    BCLog::OutSummary("Model created");

    // -------------------
    //Run Poisson likelihood
    BCLog::OutSummary("Running likelihood");
    m.MarginalizeAll(BCIntegrate::kMargMetropolis);
    m.FindMode( m.GetBestFitParameters() );
    m.PrintAllMarginalized(m.GetSafeName() + "_plots.pdf");
    m.PrintKnowledgeUpdatePlots(m.GetSafeName() + "_update.pdf");

    TH1D* h_nP = (TH1D*)m.GetMarginalizedHistogram("nP")->Clone();
    Normalize(h_nP);

    TF1* bestfit = m.GetBestFit();
    bestfit->SetLineStyle(7);
    m.PrintSummary();

    //Close log file
    BCLog::OutSummary("Exiting");
    BCLog::CloseLog();
}