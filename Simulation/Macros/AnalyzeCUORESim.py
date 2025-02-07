import uproot
import hist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import h5py as h5
import awkward as ak
import glob
import itertools
import pickle
import random
from tqdm import tqdm

class QShieldsOutput:
    def __init__(self, fileNamePattern, segLabelPath='/global/homes/v/vsharma2/TriProtonDecay/Simulation/Model/segLabelDict.pkl', numChainsPerFile=0):
        self.fileNamePattern = fileNamePattern
        self.numChainsPerFile = numChainsPerFile
        self.segLabelPath = segLabelPath

    def PrintTest(self):
        '''Test function'''
        print('filename pattern is ' + self.fileNamePattern)
        
    def AddFiles(self):
        '''Adds files with input file name pattern and converts to pandas dataframe. Also updates chain numbers to avoid overlap 
        between multiple files'''

        #Converting cuore-daq.map to dictionary with mc channels as keys and daq channels as values
        daqMapdf = pd.read_csv("./cuore-daq.map", delimiter='\t', header=None)
        daqMapdf = daqMapdf.drop(daqMapdf.columns[[2,3,4]], axis=1)
        daqMapdf.columns = ['mc', 'daq']
        daqMap = daqMapdf.set_index('mc')['daq'].to_dict();

        files = sorted(glob.glob(self.fileNamePattern))
        df = pd.DataFrame({'Channel': pd.Series(dtype='int32'),
                       'DAQChannel': pd.Series(dtype='int32'),
                       'ChainNumber': pd.Series(dtype='uint64'),
                       'UniversalChainNumber': pd.Series(dtype='uint64'),
                       'DepositedEnergy': pd.Series(dtype='float64'),
                       'EnergyDepositedInCopper': pd.Series(dtype='float64'),
                       'ParticleName': pd.Series(dtype='str'),
                       'DaughterName': pd.Series(dtype='str'),
                       'ParticlePositionX': pd.Series(dtype='float64'),
                       'ParticlePositionY': pd.Series(dtype='float64'),
                       'ParticlePositionZ': pd.Series(dtype='float64'),
                       'ParticleDirectionX': pd.Series(dtype='float64'),
                       'ParticleDirectionY': pd.Series(dtype='float64'),
                       'ParticleDirectionZ': pd.Series(dtype='float64'),
                       'ParticleInputEnergy': pd.Series(dtype='float64')})
        for index, f in enumerate(files):
            rootFile = uproot.open(f)
            rootTree = rootFile['qtree']
            rootTable = rootTree.arrays(['Channel', 'ChainNumber', 'DepositedEnergy', 'EnergyDepositedInCopper', 'ParticleName', 'DaughterName', 
                                     'ParticlePositionX', 'ParticlePositionY', 'ParticlePositionZ', 'ParticleDirectionX', 'ParticleDirectionY', 
                                     'ParticleDirectionZ', 'ParticleInputEnergy'], library='pd')
            rootTable['UniversalChainNumber'] = rootTable['ChainNumber'] + (index * self.numChainsPerFile)
            rootTable['DAQChannel'] = rootTable['Channel'].map(daqMap)
        
            df = pd.concat([df, rootTable], join='outer')
        return df.reset_index(drop=True)

    def AddMuonFiles(self):
        '''Adds files with input file name pattern and converts to pandas dataframe. Also updates chain numbers to avoid overlap 
        between multiple files'''
        #Converting cuore-daq.map to dictionary with mc channels as keys and daq channels as values
        daqMapdf = pd.read_csv("./cuore-daq.map", delimiter='\t', header=None)
        daqMapdf = daqMapdf.drop(daqMapdf.columns[[2,3,4]], axis=1)
        daqMapdf.columns = ['mc', 'daq']
        daqMap = daqMapdf.set_index('mc')['daq'].to_dict();

        files = sorted(glob.glob(self.fileNamePattern))
        df = pd.DataFrame({'Channel': pd.Series(dtype='int32'),
                       'DAQChannel': pd.Series(dtype='int32'),
                       'ChainNumber': pd.Series(dtype='uint64'),
                       'UniversalChainNumber': pd.Series(dtype='uint64'),
                       'DepositedEnergy': pd.Series(dtype='float64'),
                       'EnergyDepositedInCopper': pd.Series(dtype='float64'),
                       'ParticleName': pd.Series(dtype='str'),
                       'DaughterName': pd.Series(dtype='str'),
                       'ParticlePositionX': pd.Series(dtype='float64'),
                       'ParticlePositionY': pd.Series(dtype='float64'),
                       'ParticlePositionZ': pd.Series(dtype='float64'),
                       'ParticleDirectionX': pd.Series(dtype='float64'),
                       'ParticleDirectionY': pd.Series(dtype='float64'),
                       'ParticleDirectionZ': pd.Series(dtype='float64'),
                       'ParticleInputEnergy': pd.Series(dtype='float64')})
        
        totalChains = 0
        for index, f in tqdm(enumerate(files)):
            rootFile = uproot.open(f)
            rootTree = rootFile['qtree']
            rootTable = rootTree.arrays(['Channel', 'ChainNumber', 'DepositedEnergy', 'EnergyDepositedInCopper', 'ParticleName', 'DaughterName', 
                                     'ParticlePositionX', 'ParticlePositionY', 'ParticlePositionZ', 'ParticleDirectionX', 'ParticleDirectionY', 
                                     'ParticleDirectionZ', 'ParticleInputEnergy'], library='pd')

            uniqueChainNum = list(rootTable['ChainNumber'].unique())
            localChainNum = [i for i in range(1,len(uniqueChainNum)+1)]

            sorted_pairs = sorted(zip(uniqueChainNum, localChainNum), key=lambda x: x[0])
            grouped_pairs = itertools.groupby(sorted_pairs, key=lambda x: x[0])
            chainDict = {key: next(group)[1] for key, group in grouped_pairs}
            
            rootTable['UniversalChainNumber'] = rootTable['ChainNumber'].map(chainDict) + totalChains
            
            totalChains += len(uniqueChainNum)
            
            #rootTable['UniversalChainNumber'] = rootTable['ChainNumber'] + (index * self.numChainsPerFile)
            rootTable['DAQChannel'] = rootTable['Channel'].map(daqMap)
        
            df = pd.concat([df, rootTable], join='outer')
        return df.reset_index(drop=True)
    
    def AddFilesSegLabels(self):
        '''Adds files with input file name pattern and converts to pandas dataframe. Also updates chain numbers to avoid overlap 
        between multiple files. Only keeps fields relevant to segmentation task labels'''
        #Converting cuore-daq.map to dictionary with mc channels as keys and daq channels as values
        daqMapdf = pd.read_csv("./cuore-daq.map", delimiter='\t', header=None)
        daqMapdf = daqMapdf.drop(daqMapdf.columns[[2,3,4]], axis=1)
        daqMapdf.columns = ['mc', 'daq']
        daqMap = daqMapdf.set_index('mc')['daq'].to_dict();

        files = sorted(glob.glob(self.fileNamePattern))
        df = pd.DataFrame({'Channel': pd.Series(dtype='int32'),
                       'DAQChannel': pd.Series(dtype='int32'),
                       'ChainNumber': pd.Series(dtype='uint64'),
                       'UniversalChainNumber': pd.Series(dtype='uint64'),
                       'ParticlePositionX': pd.Series(dtype='float64'),
                       'ParticlePositionY': pd.Series(dtype='float64'),
                       'ParticlePositionZ': pd.Series(dtype='float64')})

        totalChains = 0
        for index, f in tqdm(enumerate(files)):
            rootFile = uproot.open(f)
            rootTree = rootFile['qtree']
            rootTable = rootTree.arrays(['Channel', 'ChainNumber', 'ParticlePositionX', 'ParticlePositionY', 'ParticlePositionZ'], library='pd')

            uniqueChainNum = list(rootTable['ChainNumber'].unique())
            localChainNum = [i for i in range(1,len(uniqueChainNum)+1)]

            sorted_pairs = sorted(zip(uniqueChainNum, localChainNum), key=lambda x: x[0])
            grouped_pairs = itertools.groupby(sorted_pairs, key=lambda x: x[0])
            chainDict = {key: next(group)[1] for key, group in grouped_pairs}
            
            rootTable['UniversalChainNumber'] = rootTable['ChainNumber'].map(chainDict) + totalChains
            
            totalChains += len(uniqueChainNum)
            
            #rootTable['UniversalChainNumber'] = rootTable['ChainNumber'] + (index * self.numChainsPerFile)
            rootTable['DAQChannel'] = rootTable['Channel'].map(daqMap)
        
            df = pd.concat([df, rootTable], join='outer')
        return df.reset_index(drop=True)
    
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
    
    @staticmethod
    def GetChannelFromPosition(posX, posY, posZ):
        verticalOffset = 1446 #CONFIRM THIS!!!!!
        channelMap = pd.read_csv('./crystal-positions.csv')
        distance = 10000000000
        tempChannel = 0
        posZ = posZ - verticalOffset #CONFIRM THIS!!!!!
        tempCoord = posX
        posX = posY
        posY = -1.0 * tempCoord
        for index, row in channelMap.iterrows():
            tempDistance = 1000*((posX-row['X'])**2 + (posY-row['Y'])**2 + (posZ-row['Z'])**2) #multiply by large value to solve precision issue?
            if(tempDistance < distance):
                distance = tempDistance
                tempChannel = row['Channel']

        return tempChannel
                    
    def GetOriginChannels(self):
        '''Gets origin channel for each ppp MC event and creates corresponding label for segmentation'''

        # Get Qshields output
        dfQshields = self.AddFilesSegLabels()
        print('Add files finished')

        numTotalEvents = len(dfQshields['UniversalChainNumber'].unique())
        #outputLabels = np.zeros((numTotalEvents, 10, 10, 13))

        chainDict = {}

        chainGroups = dfQshields.groupby('UniversalChainNumber')

        #For testing
        channelList = []

        for chainNumber, groupData in tqdm(chainGroups):
            tempPosX = groupData['ParticlePositionX'].unique()[0]
            tempPosY = groupData['ParticlePositionY'].unique()[0]
            tempPosZ = groupData['ParticlePositionZ'].unique()[0]

            #print('X: ' + str(tempPosX) + ' Y: ' + str(tempPosY) + ' Z: ' + str(tempPosZ))

            originChannel = self.GetChannelFromPosition(tempPosX, tempPosY, tempPosZ)
            channelList.append(originChannel)
            tempCoords = self.GenerateChannelMap(originChannel)
            tempLabel = np.zeros((10,10,13))

            tempLabel[tempCoords[0], tempCoords[1], tempCoords[2]] = 1
            chainDict[chainNumber] = tempLabel

            
        with open(self.segLabelPath, 'wb') as f:
            pickle.dump(chainDict, f)
            print('Segmentation Label dictionary saved to file')
        return chainDict, channelList 
            
        


class AresOutput:
    def __init__(self, aresFilePath, energyCap, efficiency=0.95, applySaturation=False, multiplicity=10, segLabelPath='/global/homes/v/vsharma2/TriProtonDecay/Simulation/Model/segLabelDict.pkl', numChainsPerFile=0):
        self.aresFilePath = aresFilePath #Path to ares input files
        self.numChainsPerFile = numChainsPerFile #Number of chains per ares file
        self.energyCap = energyCap #Maximum energy energy depositions can have
        self.segLabelPath = segLabelPath #Path to segmentation label dictionary
        #self.dictFilePath = dictFilePath
        self.applySaturation = applySaturation
        self.efficiency = efficiency
        self.multiplicity = multiplicity
    
    def AddFilesOld(self):
        '''Adds files with input file name pattern and converts to pandas dataframe. Also updates chain numbers to avoid overlap 
        between multiple files. !!!NEEDS TO BE FIXED FOR MULTIPLE MUON SIM FILES!!!'''
        files = sorted(glob.glob(self.aresFilePath))
        print('Number of files added --- ' + str(len(files)))
        df = pd.DataFrame({'Channel': pd.Series(dtype='int32'),
                       'ChainNumber': pd.Series(dtype='uint64'),
                       'UniversalChainNumber': pd.Series(dtype='uint64'),
                       'Energy': pd.Series(dtype='float64')})
        
        for index, f in enumerate(files):
            rootFile = uproot.open(f)
            rootTree = rootFile['outTree']
            rootTable = rootTree.arrays(['Channel', 'ChainNumber', 'Energy'], library='pd')
            rootTable['UniversalChainNumber'] = rootTable['ChainNumber'] + (index * self.numChainsPerFile) #NEEDS TO BE FIXED FOR MULTIPLE MUON FILES
        
            df = pd.concat([df, rootTable], join='outer')
        return df.reset_index(drop=True)
    
    def AddFiles(self):
        '''Adds files with variable number of chains. Assigns universal chain numbers the same way as AddFiles'''
        muonFiles = sorted(glob.glob(self.aresFilePath))
        print('Number of files added --- ' + str(len(muonFiles)))
        df = pd.DataFrame({'Channel': pd.Series(dtype='int32'),
                           'ChainNumber': pd.Series(dtype='uint64'),
                           'UniversalChainNumber': pd.Series(dtype='uint64'),
                           'Energy': pd.Series(dtype='float64')})
        totalChains = 0
        for index, f in tqdm(enumerate(muonFiles)):
            rootFile = uproot.open(f)
            rootTree = rootFile['outTree']
            rootTable = rootTree.arrays(['Channel', 'ChainNumber', 'Energy'], library='pd')
            
            uniqueChainNum = list(rootTable['ChainNumber'].unique())
            localChainNum = [i for i in range(1,len(uniqueChainNum)+1)]

            sorted_pairs = sorted(zip(uniqueChainNum, localChainNum), key=lambda x: x[0])
            grouped_pairs = itertools.groupby(sorted_pairs, key=lambda x: x[0])
            chainDict = {key: next(group)[1] for key, group in grouped_pairs}
            
            rootTable['UniversalChainNumber'] = rootTable['ChainNumber'].map(chainDict) + totalChains
            
            totalChains += len(uniqueChainNum)
            

            #if index==0:
            #    rootTable['UniversalChainNumber'] = rootTable['ChainNumber']
            #else:
            #    rootTable['UniversalChainNumber'] = rootTable['ChainNumber'] + totalChains

            df = pd.concat([df, rootTable], join='outer')
            #print('Added file ' + str(index))
            #print(str(df.shape[0]))
        return df.reset_index(drop=True)

    @staticmethod
    def saturationFilter(value, energyCap):
        if value > 12.0:
            if value < 14.0:
                dice = random.uniform(0, 1)
                if dice > 0.086:
                    value = energyCap
                    #print(dice)
            if value < 16.0:
                dice = random.uniform(0, 1)
                if dice > 0.181:
                    value = energyCap
                    #print(dice)
            if value < 18.0:
                dice = random.uniform(0, 1)
                if dice > 0.317:
                    value = energyCap
                    #print(dice)
            if value < 20.0:
                dice = random.uniform(0, 1)
                if dice > 0.479:
                    value = energyCap
                    #print(dice)
            if value < 22.0:
                dice = random.uniform(0, 1)
                if dice > 0.602:
                    value = energyCap
                    #print(dice)
            if value < 24.0:
                dice = random.uniform(0, 1)
                if dice > 0.692:
                    value = energyCap
                    #print(dice)
            if value > energyCap:
                value = energyCap
                #print('Greater than 22.0')
        return value

    @staticmethod
    def ApplyCuts(df, efficiency=0.96, applySaturation=False, energyCap=12.0, multiplicity=10):
        '''Applies cuts to MC pandas dataframe based on energy values, multiplicity, dead channels and various data processing related efficiencies'''

        #Removing dead channels
        deadChannels =[117, 169, 792, 812, 923]
        df = df[~df['Channel'].isin(deadChannels)]

        #Applying efficiency
        removalProbability = 1.0 - efficiency
        randomNumbers = np.random.rand(len(df))
        df = df[randomNumbers >= removalProbability]
       
        #Applying energy cuts
        df = df[df['Energy'] >= 0.35]
        df.reset_index(drop=True, inplace=True)

        #Applying cuts based on multiplicity
        df = df.groupby('UniversalChainNumber').filter(lambda x: len(x) >= multiplicity)

        #Applying saturation curve
        if(applySaturation):
            df['Energy'] = df['Energy'].apply(AresOutput.saturationFilter, energyCap=energyCap)

        #Capping energy in ares output to account for saturation
        if(not applySaturation):
            df['Energy'] = df['Energy'].apply(lambda x, cap=energyCap: min(x, cap))

        #Setting small negative energies to zero
        df['Energy'] = df['Energy'].apply(lambda x: max(x, 0)) 

        #Scaling down energy to [0,1] range
        df['Energy'] = df['Energy']/energyCap

        #print('Experimental run -- scaling from 0 to 1.2')
        #df['Energy'] = df['Energy']*1.2

        return df

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


    def ConvertAresToNP(self):
        '''Converts ares output to 3d matrix after normalization to .npy binary format'''
        dfAresCopy = self.AddFiles()
        print('Add files finished')
        #dfAresCopy = dfAres.copy()

        dfAresCopy = self.ApplyCuts(dfAresCopy, self.efficiency, self.applySaturation, self.energyCap, self.multiplicity)

        #Normalizing energies
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x, cap=self.energyCap: min(x, cap)) # capping energy in ares output to account for saturation
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x: max(x, 0)) # setting small negative energies to zero
        #dfAresCopy['Energy'] = dfAresCopy['Energy']/self.energyCap # scaling down energy to [0,1] range
        print('Finished normalizing energies')

        uniqueChains = dfAresCopy['UniversalChainNumber'].unique()
        numTotalEvents = len(dfAresCopy['UniversalChainNumber'].unique()) 
        outputArray = np.zeros((numTotalEvents, 10, 10, 13)) #initializing output numpy array
        print('Initialized output array')
        #print('Removing ' + str(int((1-self.efficiency)*988)) + ' channels due to base cuts')

        iter=0 # counter over training examples
        for index in tqdm(uniqueChains):
            #if(index%1000==0):
                #print('Processing chain ' + str(index))
            dfTemp = dfAresCopy.query(f'UniversalChainNumber=={index}', engine='python')
            for i, r in dfTemp.iterrows():
                tempChannel = r['Channel']
                tempEnergy = r['Energy']
                tempCoords = self.GenerateChannelMap(tempChannel)
                #print(str(tempCoords[0])+ '---' + str(tempCoords[1]) + '---' + str(tempCoords[2]))
                #print(type(tempCoords))
                outputArray[iter,tempCoords[0], tempCoords[1], tempCoords[2]] = tempEnergy
            iter=iter+1
            #Applying basecut efficiency
            #selectedChannels = np.random.choice(np.arange(1,989), size=int((1-self.efficiency)*988), replace=False)
            
            #for ch in selectedChannels:
        #         cutCoords = self.GenerateChannelMap(ch)
        #         outputArray[iter, cutCoords[0], cutCoords[1], cutCoords[2]] = 0.0

        #     if np.count_nonzero(outputArray[iter]) > 15:
        #         iter=iter+1
        #     else:
        #         outputArray[iter] = np.zeros((10,10,13))

        # nonZeroMask = np.any(outputArray != 0, axis=(1, 2, 3))
        # outputArray = outputArray[nonZeroMask]

        return outputArray

    @staticmethod
    def saveArrayToH5(filePath, index, arrayData):
        with h5.File(filePath, 'a') as hdf5_file:
            hdf5_file.create_dataset(str(index), data=arrayData)

    def ConvertArestoDict(self):
        '''Convert ares output to hdf5 file format, saving ppp decays as 3d matrices with identifier indices'''
        dfAresCopy = self.AddFiles()
        print('Add files finished')
        #dfAresCopy = dfAres.copy()

        dfAresCopy = self.ApplyCuts(dfAresCopy)

        #Normalizing energies
        dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x, cap=self.energyCap: min(x, cap)) # capping energy in ares output to account for saturation
        dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x: max(x, 0)) # setting small negative energies to zero
        dfAresCopy['Energy'] = dfAresCopy['Energy']/self.energyCap # scaling down energy to [0,1] range
        print('Finished normalizing energies')

        uniqueChains = dfAresCopy['UniversalChainNumber'].unique()
        numTotalEvents = len(dfAresCopy['UniversalChainNumber'].unique()) 
        #outputArray = np.zeros((numTotalEvents, 10, 10, 13)) #initializing output numpy array
        tempArray = np.zeros((10,10,13))
        print('Initialized output array')

        outputDict = {}

        iter=0 # counter over training examples
        for index in tqdm(uniqueChains):
            #if(index%1000==0):
                #print('Processing chain ' + str(index))
            dfTemp = dfAresCopy.query(f'UniversalChainNumber=={index}', engine='python')
            for i, r in dfTemp.iterrows():
                tempChannel = r['Channel']
                tempEnergy = r['Energy']
                tempCoords = self.GenerateChannelMap(tempChannel)
                #print(str(tempCoords[0])+ '---' + str(tempCoords[1]) + '---' + str(tempCoords[2]))
                #print(type(tempCoords))
                tempArray[tempCoords[0], tempCoords[1], tempCoords[2]] = tempEnergy
            iter=iter+1
            # #Applying basecut efficiency
            # selectedChannels = np.random.choice(np.arange(1,989), size=int((1-self.efficiency)*988), replace=False)
            # for ch in selectedChannels:
            #     cutCoords = self.GenerateChannelMap(ch)
            #     tempArray[iter, cutCoords[0], cutCoords[1], cutCoords[2]] = 0.0

            # outputDict[index] = tempArray
            # #self.saveArrayToH5(self.dictFilePath, index, tempArray)
            # tempArray = np.zeros((10,10,13))
            #iter=iter+1
        #with open(self.dictFilePath, 'wb') as f:
            #pickle.dump(outputDict, f)
            #print('Ares output dictionary saved to file')
        return outputDict


    def ConvertAresToNPSeg(self):
        '''Convert ares output to 3d matrix after normalization to .npy binary formay. Also processes segmentation labels'''
        dfAresCopy = self.AddFiles()
        print('Add files finished')
        #dfAresCopy = dfAres.copy()

        dfAresCopy = self.ApplyCuts(dfAresCopy)

        with open(self.segLabelPath, 'rb',) as f:
            segLabelDict = pickle.load(f)

        #Normalizing energies
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x, cap=self.energyCap: min(x, cap)) # capping energy in ares output to account for saturation
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x: max(x, 0)) # setting small negative energies to zero
        #dfAresCopy['Energy'] = dfAresCopy['Energy']/self.energyCap # scaling down energy to [0,1] range
        print('Finished normalizing energies')

        uniqueChains = dfAresCopy['UniversalChainNumber'].unique()
        numTotalEvents = len(dfAresCopy['UniversalChainNumber'].unique()) 
        outputArray = np.zeros((numTotalEvents, 10, 10, 13)) #initializing output numpy array
        segLabelArray = np.zeros((numTotalEvents, 10, 10, 13)) #initializing segmentation label array
        print('Intialized output and seg label array')

        iter=0 # counter over training examples
        for index in tqdm(uniqueChains):
            if(index%1000==0):
                print('Processing chain ' + str(index))
            segLabelArray[iter] = segLabelDict[index]
            dfTemp = dfAresCopy.query(f'UniversalChainNumber=={index}', engine='python')
            for i, r in dfTemp.iterrows():
                tempChannel = r['Channel']
                tempEnergy = r['Energy']
                tempCoords = self.GenerateChannelMap(tempChannel)
                #print(str(tempCoords[0])+ '---' + str(tempCoords[1]) + '---' + str(tempCoords[2]))
                #print(type(tempCoords))
                outputArray[iter,tempCoords[0], tempCoords[1], tempCoords[2]] = tempEnergy
            iter=iter+1
        return outputArray, segLabelArray


    @staticmethod
    def CombineClasses(array1, array2, exampleFilePath, labelFilePath):
        '''Assigns labels to two numpy arrays corresponding to two input classes, combines them and shuffles them. Saves the two classes in numpy binary files'''
        #Assign labels to input arrays
        array1Labels = np.ones(array1.shape[0])
        array2Labels = np.zeros(array2.shape[0])

        #Combine events from two arrays
        combinedEvents = np.concatenate((array1, array2), axis=0)
        combinedLabels = np.concatenate((array1Labels, array2Labels), axis=0)

        permutedIndices = np.random.permutation(combinedEvents.shape[0])

        #Shuffle both combined_events and combined_labels using the same permutation
        shuffledExamples = combinedEvents[permutedIndices]
        shuffledLabels = combinedLabels[permutedIndices]

        np.save(exampleFilePath, shuffledExamples)
        np.save(labelFilePath, shuffledLabels)        

        return shuffledExamples, shuffledLabels

    @staticmethod
    def CombineSegClasses(array1, array2, array3, exampleFilePath, labelFilePath, segLabelFilePath):
        '''Assigns labels to two numpy arrays corresponding to two input classes, combines them and shuffles them. Also saves segmentation labels
        permuted the same way as the two numpy arrays
        array1: ppp events
        array2: muon events
        array3: segmentation labels'''
        
        #Assign labels to input arrays
        array1Labels = np.ones(array1.shape[0]) #ppp decay events
        array2Labels = np.zeros(array2.shape[0]) ##Muon events

        #Dummy labels to take place of muon event locations
        dummyLabelArray = np.ones((array3.shape[0], array3.shape[1], array3.shape[2],array3.shape[3]))
        dummyLabelArray = -1 * dummyLabelArray

        combinedSegLabels = np.concatenate((array3,dummyLabelArray), axis=0)

        #Combine events from two arrays
        combinedEvents = np.concatenate((array1, array2), axis=0)
        combinedLabels = np.concatenate((array1Labels, array2Labels), axis=0)

        permutedIndices = np.random.permutation(combinedEvents.shape[0])

        #Shuffle both combined_events and combined_labels using the same permutation
        shuffledExamples = combinedEvents[permutedIndices]
        shuffledLabels = combinedLabels[permutedIndices]
        shuffledSegLabels = combinedSegLabels[permutedIndices]

        np.save(exampleFilePath, shuffledExamples)
        np.save(labelFilePath, shuffledLabels)        
        np.save(segLabelFilePath, shuffledSegLabels)

        return shuffledExamples, shuffledLabels, shuffledSegLabels
    
    @staticmethod
    def convertDictToArray(inputDict):
        '''Converts an event dictionary to numpy arrays and list of indices'''
        # Extract indices and matrices from the dictionary
        indices = list(inputDict.keys())
        matrices = list(inputDict.values())

        # Determine the shape of the 4D array based on the shape of the individual matrices
        matrixShape = matrices[0].shape
        arrayShape = (len(indices),) + matrixShape

        # Initialize the 4D array with zeros
        resultArray = np.zeros(arrayShape)

        # Fill the 4D array with the matrices in the same order as the indices
        for i, index in enumerate(indices):
            resultArray[i, :, :, :] = matrices[i]

        return resultArray, indices

    @staticmethod
    def CombineDicts(dict1, dict2, exampleFilePath, labelFilePath, indexFilePath):
        '''Combines two event dictionaries to return shuffled training examples, shuffled labels and shuffled event indices'''
        array1, indices1 = AresOutput.convertDictToArray(dict1)
        array2, indices2 = AresOutput.convertDictToArray(dict2)
    
        #print('Dictionary conversion finished')

        array2 = array2[0:array1.shape[0], :, :, :]
        #print('ppp events -- ' + str(array1.shape[0]) + ' muon events -- ' + str(array2.shape[0]))

        array1Labels = np.ones(array1.shape[0])
        array2Labels = np.zeros(array2.shape[0])

        #Combine events from two arrays
        combinedEvents = np.concatenate((array1, array2), axis=0)
        combinedLabels = np.concatenate((array1Labels, array2Labels), axis=0)

        #print('Combined events and labels')

        indices1Len = len(indices1)
        indices2Mod = [element + indices1Len for element in indices2]

        combinedIndices = indices1 + indices2Mod

        permutations = np.random.permutation(combinedEvents.shape[0])

        #Shuffle both combined_events and combined_labels using the same permutation
        shuffledExamples = combinedEvents[permutations]
        shuffledLabels = combinedLabels[permutations]
        shuffledIndices = [combinedIndices[i] for i in permutations]

        #print('Permutated examples, labels, and indices')

        np.save(exampleFilePath, shuffledExamples)
        np.save(labelFilePath, shuffledLabels)  

        #print('Saved numpy arrays')

        with open(indexFilePath, 'w') as indexFile:
            for item in shuffledIndices:
                indexFile.write(str(int(item)) + '\n')      
        
        #print('Saved indices file')

        return shuffledExamples, shuffledLabels, shuffledIndices

    @staticmethod
    def BiasTest(array1, array2, injectionRate):
        '''Injects a preset number of events from array1 and inserts them in array2. Also shuffles the resultant array'''
         # Get the shape of the input arrays
        shape1 = array1.shape
        shape2 = array2.shape

        # Extract the events from the first event array and randomize their order
        selected_indices = np.random.choice(shape1[0], size=injectionRate, replace=False)
        selected_arrays = array1[selected_indices]

        # Generate random indices for insertion into the second event array
        random_indices = np.random.randint(0, shape2[0], size=injectionRate)

        # Insert the selected arrays into random locations in the second 4D array
        np.insert(array2, random_indices, selected_arrays)

        # Reshape and shuffle the second 4D array
        shuffled_array2 = np.random.permutation(array2)

        return shuffled_array2
    
    def ConvertAresToNPExp(self):
        '''Converts ares output to 3d matrix after normalization to .npy binary format'''
        dfAresCopy = self.AddFiles()
        print('Add files finished')
        #dfAresCopy = dfAres.copy()

        dfAresCopy = self.ApplyCuts(dfAresCopy, self.efficiency, self.applySaturation, self.energyCap)

        #Normalizing energies
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x, cap=self.energyCap: min(x, cap)) # capping energy in ares output to account for saturation
        #dfAresCopy['Energy'] = dfAresCopy['Energy'].apply(lambda x: max(x, 0)) # setting small negative energies to zero
        #dfAresCopy['Energy'] = dfAresCopy['Energy']/self.energyCap # scaling down energy to [0,1] range
        print('Finished normalizing energies')

        uniqueChains = dfAresCopy['UniversalChainNumber'].unique()
        numTotalEvents = len(dfAresCopy['UniversalChainNumber'].unique()) 
        outputArray = np.zeros((numTotalEvents, 10, 10, 14)) #initializing output numpy array
        print('Initialized output array')
        print('Removing ' + str(int((1-self.efficiency)*988)) + ' channels due to base cuts')

        iter=0 # counter over training examples
        for index in tqdm(uniqueChains):
            #if(index%1000==0):
                #print('Processing chain ' + str(index))
            dfTemp = dfAresCopy.query(f'UniversalChainNumber=={index}', engine='python')
            for i, r in dfTemp.iterrows():
                tempChannel = r['Channel']
                tempEnergy = r['Energy']
                tempCoords = self.GenerateChannelMap(tempChannel)
                #print(str(tempCoords[0])+ '---' + str(tempCoords[1]) + '---' + str(tempCoords[2]))
                #print(type(tempCoords))
                outputArray[iter,tempCoords[0], tempCoords[1], tempCoords[2]] = tempEnergy

            #Applying basecut efficiency
            selectedChannels = np.random.choice(np.arange(1,989), size=int((1-self.efficiency)*988), replace=False)
            
            for ch in selectedChannels:
                cutCoords = self.GenerateChannelMap(ch)
                outputArray[iter, cutCoords[0], cutCoords[1], cutCoords[2]] = 0.0

            if np.count_nonzero(outputArray[iter]) > 10:
                iter=iter+1
            else:
                outputArray[iter] = np.zeros((10,10,14))

        return outputArray