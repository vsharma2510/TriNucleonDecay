import BiasTest as bt
import sys
import time

start_time = time.time()
nP = int(sys.argv[1])
print(f'Number of injected ppp decays --- {nP}')

muonFilePath = '/pscratch/sd/v/vsharma2/TriNucleonDecay/CNN_Input/LIV/Muon_BiasTest_Sample_200k.npy'
pppFilePath = '/pscratch/sd/v/vsharma2/TriNucleonDecay/CNN_Input/LIV/ppp_BiasTest_Sample_200k.npy'
modelFilePath = '/pscratch/sd/v/vsharma2/TriNucleonDecay/CNN_Model/ppp_classification_model_bias_test.h5'
outputFilePath = f'../Output/BiasTestResults/InferenceResults_{nP}_350keV_10M.root'
nMu = 12000

# print('Running inference')
biasTest = bt.BiasTest(muonFilePath=muonFilePath, pppFilePath=pppFilePath, modelFilePath=modelFilePath, outputFilePath=outputFilePath, nMu=nMu, nP=nP, numExp=10000)
# biasTest.RunInference()
# print('Finished')

print('Running inference')
biasTest.RunInference()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")
print('Finished')