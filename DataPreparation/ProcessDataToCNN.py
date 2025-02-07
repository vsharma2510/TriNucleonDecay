import uproot
import hist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import awkward as ak
import glob
# import AnalyzeCUORESim as an
from IPython.display import display
from tqdm import tqdm
import itertools

#Function to merge saturated events
#Function to remove contaminated runs

class DatasetClusters:
    def __init__(self, dataFilePath,  dataset):
        self.dataFilePath = dataFilePath
        self.dataset = dataset
        #self.saturatedFilePath = f'/pscratch/sd/v/vsharma2/TriNucleonDecay/Data/ds{self.dataset}_sat/output/Dataset-{self.dataset}_RunNumber-*_Coincidence-NoAppliedCoincidence_Validation-NoAppliedValidationCalib.root'

    def GetSaturated(self):
        saturatedFilePath = f'/pscratch/sd/v/vsharma2/TriNucleonDecay/Data/ds{self.dataset}_sat/output/Dataset-{self.dataset}_RunNumber-*_Coincidence-NoAppliedCoincidence_Validation-NoAppliedValidationCalib.root'
        satFiles = sorted(glob.glob(saturatedFilePath))
        print(f'Number of files added --- {len(satFiles)}')
        df = pd.DataFrame({'IsSatHigh9200mV': pd.Series(dtype='bool'),
                           'Run': pd.Series(dtype='uint64'),
                           'EventNumber': pd.Series(dtype='uint64')})
        
        for index, f in tqdm(enumerate(satFiles)):
            rootFile = uproot.open(f)
            rootTree = rootFile['tree']
            rootTable = rootTree.arrays(['IsSatHigh9200mV', 'Run', 'EventNumber'], library='pd')

            df = pd.concat([df, rootTable], join='outer')
        
        df = df[df['IsSatHigh9200mV']]
        return df.reset_index(drop=True)

    @staticmethod
    def ProcessDataset(df):
        df = df.drop(['Outside?', 'X', 'Y', 'Z', 'MC Channel', 'CoincTime', 'Baseline', 'MaxToBaseline', 'BaselineRMS', 'OFRiseTime', 'OFDecayTime',
                    'OFdelay', 'OFChi2', 'Multiplicity', 'PCANorm', 'Tower', 'Floor', 'BoxFilter', 'Flag'], axis=1) 

        df = df.query('NumPulses==1', engine='python')
        df = df.query('SingleTrigger==True', engine='python')
        df = df.query('BaselineSlope > -0.01 and BaselineSlope < 0.01 ')
        #valueCounts = df['ChainNumber'].value_counts()

        dfSorted = df.sort_values(by=['ChainNumber', 'Time'])
        dfSorted['diff'] = df.groupby('ChainNumber')['Time'].transform(lambda x: x - x.iloc[0])
        dfSorted = dfSorted.query('diff < 0.075', engine='python')

        valueCounts = dfSorted['ChainNumber'].value_counts()
        dfM = dfSorted[dfSorted['ChainNumber'].isin(valueCounts.index[valueCounts >= 10])]

        #TODO!!! Need to add code to remove contaminated runs

        return dfM
    
    @staticmethod
    def GenerateChannelMap(inputChannel):
        '''Convert channel number to position in 3d array'''
        baseChannelMap = ({963:(0,2,0), 950:(0,3,0), 105:(0,4,0), 144:(0,5,0), 157:(0,6,0), 196:(0,7,0),
                          976:(1,2,0), 937:(1,3,0), 118:(1,4,0), 131:(1,5,0), 170:(1,6,0), 183:(1,7,0),
                          911:(2,1,0), 898:(2,2,0), 859:(2,3,0), 846:(2,4,0), 1:(2,5,0), 40:(2,6,0), 53:(2,7,0), 92:(2,8,0),
                          924:(3,1,0), 885:(3,2,0), 872:(3,3,0), 833:(3,4,0), 14:(3,5,0), 27:(3,6,0), 66:(3,7,0), 79:(3,8,0),
                          599:(4,0,0), 586:(4,1,0), 807:(4,2,0), 794:(4,3,0), 209:(4,4,0), 248:(4,5,0), 261:(4,6,0), 300:(4,7,0), 313:(4,8,0), 352:(4,9,0),
                          612:(5,0,0), 573:(5,1,0), 820:(5,2,0), 781:(5,3,0), 222:(5,4,0), 235:(5,5,0), 274:(5,6,0), 287:(5,7,0), 326:(5,8,0), 339:(5,9,0),
                          703:(6,1,0), 690:(6,2,0), 651:(6,3,0), 638:(6,4,0), 365:(6,5,0), 404:(6,6,0), 417:(6,7,0), 456:(6,8,0),
                          716:(7,1,0), 677:(7,2,0), 664:(7,3,0), 625:(7,4,0), 378:(7,5,0), 391:(7,6,0), 430:(7,7,0), 443:(7,8,0),
                          755:(8,2,0), 742:(8,3,0), 469:(8,4,0), 508:(8,5,0), 521:(8,6,0), 560:(8,7,0), 
                          768:(9,2,0), 729:(9,3,0), 482:(9,4,0), 495:(9,5,0), 534:(9,6,0), 547:(9,7,0)})

        baseChannelQ = inputChannel//13
        baseChannelR = inputChannel%13
        if baseChannelR==0:
            baseChannel = inputChannel - 12
        else:    
            baseChannel = (baseChannelQ*13)+1

        baseChannelCoords = list(baseChannelMap[baseChannel])
        inputChannelCoords = baseChannelCoords.copy()
        inputChannelCoords[2] += int(inputChannel-baseChannel)

        return tuple(inputChannelCoords)
    

    def ConvertDataToCNN(self):
        mainDir = '/pscratch/sd/v/vsharma2/TriNucleonDecay/Data/ClusterOutput/cluster_out/'
        dfSat = self.GetSaturated()
        dfData = pd.read_csv(f'{mainDir}/ds{self.dataset}/ds{self.dataset}_75.0msClustering350.0keVThreshold_test_Clustered.csv', engine='python')

        if self.dataset==3810:
            runsToRemove = [353159, 353168, 353169, 353171, 353177, 353178, 353185, 353197]
            dfData = dfData[~dfData['Run'].isin(runsToRemove)]
        if self.dataset==3815:
            runsToRemove = [353439, 353440, 353455]
            dfData = dfData[~dfData['Run'].isin(runsToRemove)]
        if self.dataset==3824:
            runsToRemove = [352103, 352106, 352112, 352132, 352122]
            dfData = dfData[~dfData['Run'].isin(runsToRemove)]

        #Apply data selections
        dfDataP = self.ProcessDataset(dfData)

        #Merge cluster data with saturation data
        dfMerged = pd.merge(dfDataP, dfSat[['Run', 'EventNumber', 'IsSatHigh9200mV']], on=['Run', 'EventNumber'], how='left')
        dfMerged['IsSatHigh9200mV'] = dfMerged['IsSatHigh9200mV'].fillna(False)

        #Convert energy to CNN input
        dfMerged['Energy'] = dfMerged.apply(lambda row: 1 if row['IsSatHigh9200mV'] else row['Energy']/12000, axis=1)
        dfMerged = dfMerged.query('Energy <= 1', engine='python')

        uniqueChains = dfMerged['ChainNumber'].unique()
        numTotalChains = len(dfMerged['ChainNumber'].unique())

        outputArray = np.zeros((numTotalChains, 10, 10, 13))

        iter=0
        for index in tqdm(uniqueChains):
            dfTemp = dfMerged.query(f'ChainNumber=={index}', engine='python')
            for i,r in dfTemp.iterrows():
                tempChannel = r['Channel']
                tempEnergy = r['Energy']
                tempCoords = self.GenerateChannelMap(tempChannel)
                outputArray[iter, tempCoords[0], tempCoords[1], tempCoords[2]] = tempEnergy
            iter=iter+1

        np.save(f'/pscratch/sd/v/vsharma2/TriNucleonDecay/Data/CNN_Input/{self.dataset}.npy', outputArray)
        return outputArray, dfMerged

        #return dfMerged
        