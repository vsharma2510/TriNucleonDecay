import numpy as np
#import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
from tensorflow import keras
import uproot
import pandas as pd
from datetime import datetime

#nPList = [0,1,2,3,4,5,6,7,8,9]

class BiasTest:
    def __init__(self, muonFilePath, pppFilePath, modelFilePath, outputFilePath, nMu=0, nP=0, numExp=10000):
        self.muonFilePath = muonFilePath
        self.pppFilePath = pppFilePath
        self.modelFilePath = modelFilePath
        self.nMu = nMu
        self.nP = nP
        self.numExp = numExp
        self.outputFilePath = outputFilePath

        # if nP is None:
        #     nP = nPList
        # self.nP = nP

    def PrepareMC(self, muArray, pppArray, pppInjected):
        # muArray = np.load(self.muonFilePath)
        # pppArray = np.load(self.pppFilePath)
        muShape = muArray.shape[0]
        pppShape = pppArray.shape[0]

        muSampleShape = np.random.poisson(self.nMu)
        pppSampleShape = np.random.poisson(pppInjected)

        # Extract the events from the ppp event array and randomize their order
        pppSelectedIndices = np.random.choice(pppShape, size=pppSampleShape, replace=False)
        pppSelectedArray = pppArray[pppSelectedIndices]

        #Extract events from muon array to prepare muon sample
        muSelectedIndices = np.random.choice(muShape, size=muSampleShape, replace=False)
        muSelectedArray = muArray[muSelectedIndices]

        combinedArray = np.concatenate((muSelectedArray, pppSelectedArray), axis=0)

        # Reshape and shuffle the resultant array
        shuffledMuArray = np.random.permutation(combinedArray)

        return shuffledMuArray

    def RunInference(self):
        model = keras.models.load_model(self.modelFilePath)
        muArray = np.load(self.muonFilePath)
        pppArray = np.load(self.pppFilePath)

        df = pd.DataFrame({'injectedSignal': pd.Series(dtype='int32'), 'nObserved': pd.Series(dtype='int32')})
        
        for i in range(self.numExp):
            print(f'Toy {i}')
            expSample = self.PrepareMC(muArray, pppArray, self.nP)
            modelPredProb = model.predict(expSample, batch_size=4096, verbose=0)
            modelPred = modelPredProb > 0.5
            modelPred = modelPred.astype(int)
            numPred = np.count_nonzero(modelPred==1)

            newRow = {'injectedSignal': self.nP, 'nObserved': numPred}
            df.loc[len(df)] = newRow

        currentDateTime = datetime.now()
        formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H:%M:%S")

        with uproot.recreate(self.outputFilePath) as outFile:
            outFile['tree'] = df
            outFile['infoTree'] = f'Muon sample size: {self.nMu} \n Number of experiments: {self.numExp} \n Muon file path: {self.muonFilePath} \n PPP file path: {self.pppFilePath} \n Model file path: {self.modelFilePath} \n Time: {formattedDateTime}'