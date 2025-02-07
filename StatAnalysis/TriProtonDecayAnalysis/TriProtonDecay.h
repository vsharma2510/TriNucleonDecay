#ifndef __BAT__TRIPROTONDECAY__H
#define __BAT__TRIPROTONDECAY__H

#include <BAT/BCModel.h>

#include <string>
#include <vector>
#include <map>

class TriProtonDecay : public BCModel
{
public:
    //enum FitMethod{ kBinomial, kMultinomial, kPoisson };
    //TODO:Include any public variables here
    
private:
    int nObs; //Number of ppp decay candidates
    double LogFactorial( double n );
    double LogPoisson( double n,
		       double lambda );
    
public:

    TriProtonDecay(const std::string& name);

    ~TriProtonDecay();

    double LogLikelihood(const std::vector<double>& pars);

    //void CalculateObservables(const std::vector<double>& pars);
    
    //void SetFitMethod( FitMethod method );

    //TH1D* GetData();
    //TF1* GetBestFit();
};

#endif