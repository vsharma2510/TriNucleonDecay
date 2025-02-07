// ***************************************************************
// This file was created using the bat-project script.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#include "BAT/BCConstantPrior.h"
#include "BAT/BCGaussianPrior.h"
#include "TriProtonDecay.h"

// #include <BAT/BCMath.h>

// ---------------------------------------------------------
TriProtonDecay::TriProtonDecay(const std::string& name)
    : BCModel(name), fNObs(0)
{
    // Define parameters here in the constructor.
    // Also define their priors, if using built-in priors.
    // For example:
    // AddParameter("mu", -2, 1, "#mu", "[GeV]");
    // GetParameters.Back().SetPrior(new BCGaussianPrior(-1, 0.25));

    // Define observables here, too. For example:
    // AddObservable("mu_squared", 1, 4, "#mu^{2}", "[GeV^{2}]");

    //nObs = 845; //TODO: Implement code to get nObs from CNN model

    //Create model parameter for number of ppp decays
    double minNp = 0;
    double maxNp = 100; //TODO: Figure out an intelligent way to set this
    AddParameter("nP", minNp, maxNp, "n_{ppp}");
    GetParameters().Back().SetNbins(300);
    GetParameters().Back().SetPrior( new BCConstantPrior() );
    
    //Create model parameter for number of muon decays
    double minMu = 1100;
    double maxMu = 1500; //TODO: Get from data?
    double meanMu = 1305; //TODO: Get from data?
    double sigmaMu = 36; //TODO: Get from data?
    AddParameter("nMu", minMu, maxMu, "n_{\\mu}");
    GetParameters().Back().SetNbins(300);
    GetParameters().Back().SetPrior( new BCGaussianPrior(meanMu, sigmaMu) );
   
    //Create model parameter for ppp efficiency
    //Range should be intersection between physical limits and 5 sigma
    //Set bins to 300
    double minEp = 0.5;
    double maxEp = 0.8;
    double meanEp = 0.6692; //TODO: Get from MC peformance
    double sigmaEp =0.0095; //TODO: Get from MC performance
    AddParameter("eP", minEp, maxEp, "\\epsilon_{p}");
    GetParameters().Back().SetNbins(300);
    GetParameters().Back().SetPrior( new BCGaussianPrior(meanEp, sigmaEp) );
   

    //Create model parameter for muon "efficiency"
    double minEmu = 0.0;
    double maxEmu = 0.1;
    double meanEmu = 0.0327; //TODO: Get from MC peformance
    double sigmaEmu = 0.0048; //TODO: Get from MC performance
    AddParameter("eMu", minEmu, maxEmu, "\\epsilon_{\\mu}");
    GetParameters().Back().SetNbins(300);
    GetParameters().Back().SetPrior( new BCGaussianPrior(meanEmu, sigmaEmu) );

    double minD = 0;
    double maxD = 2e-25;
    AddObservable("DecayRate" ,minD, maxD, "\\Gamma_{ppp}", "[ yr^{-1} ]");
    GetObservables().Back().SetNbins(300);
    
}

// ---------------------------------------------------------
TriProtonDecay::~TriProtonDecay()
{
    // destructor
}

// ---------------------------------------------------------
void TriProtonDecay::SetNObs(unsigned nobs)
{
    // set number of observed events
    fNObs = nobs;
}

// ---------------------------------------------------------
double TriProtonDecay::LogLikelihood(const std::vector<double>& pars)
{
    // return the log of the conditional probability p(data|pars).
    // This is where you define your model.
    // BCMath contains many functions you will find helpful.

    double logL = 0.;

    double nP = (int)( pars[0] );
    double nMu = (int)( pars[1] );
    double eP = pars[2];
    double eMu = pars[3];

    //Defining the log likelihood for poisson counting
    double lambda = (eP*nP) + (eMu*nMu);
    logL = LogPoisson(fNObs, lambda);

    return logL;
}

// Computes the logarithm of the factorial.
double TriProtonDecay::LogFactorial( double n )
{
    if( n <= 1. )
        return 0.;
    return log(n) + LogFactorial(n-1.);
}

double TriProtonDecay::LogPoisson( double n,
					double lambda )
{
    // Faster formula, neglecting the factorial term which does not depend on lambda.
    return -lambda + n * log(lambda);
    
    // Full formula, including factorial term
    //return -lambda + n * log(lambda) - LogFactorial(n);
}

// ---------------------------------------------------------
// double TriProtonDecay::LogAPrioriProbability(const std::vector<double>& pars)
// {
//     // return the log of the prior probability p(pars)
//     // If you use built-in priors, leave this function commented out.
// }

// ---------------------------------------------------------
void TriProtonDecay::CalculateObservables(const std::vector<double>& pars)
{
    // Calculate and store obvserables. For example:
    GetObservable(0) = (pars[0]*130)/(236.5*0.34*1000*(6.022*1e23));
    return;
}


