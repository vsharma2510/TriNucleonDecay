#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:34:38 2022
Script to plot event total energies and times
@author: Vivek Sharma
"""
import json as js
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Opening json file
filepath = '/global/projecta/projectdirs/cuore/scratch/vsharma/Tri_proton_decay/High_multiplicity_events_study/GroupedEventsAndTimesM10Count10.json'
filetext = open(filepath, 'r').read()
object = js.loads(filetext)

df = pd.DataFrame(columns = ['channel', 'energy', 'time'])

for event in object:
    df_temp = pd.DataFrame(columns = ['channel', 'energy', 'time'])
    channels = event['CrystalNumbers']
    energies = event['Energies']
    startTime = event['Time']
    timeDel = event['TimeDeltas']
    times = [i+startTime for i in timeDel]
    multiplicity = event['Multiplicity']
    energiesFiltered = [i for i in energies if i >= 0] #Removing negative values
    energiesSum = sum(energiesFiltered) 
    avgTime = startTime + (sum(timeDel)/multiplicity)
    
    df_temp['channel'] = channels
    df_temp['energy'] = energies
    df_temp['time'] = times
    df = pd.concat([df, df_temp])
    
sns.jointplot(x = df['time'], y = df['energy'], kind='hist')
plt.savefig('eventEnergiesvsTime.png')